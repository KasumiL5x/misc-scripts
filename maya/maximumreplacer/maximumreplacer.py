#
# Maximum Replacer
# Daniel Green, 2019
# GitHub: KasumiL5x

import re
import PySide2.QtCore as QC
import PySide2.QtGui as QG
import PySide2.QtWidgets as QW
import shiboken2
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMayaUI as omui
 
def get_maya_window():
	ptr = omui.MQtUtil.mainWindow()
	parent = shiboken2.wrapInstance(long(ptr), QW.QDialog)
	return parent
#end
 
class MaximumReplacer(QW.QDialog):
	def __init__(self, parent=get_maya_window()):
		QW.QDialog.__init__(self, parent=parent)
 
		# [(short_name, long_name), ...]
		self.selected_items = []
		# [(regexed_short_name, different_from_original), ...] maps 1-1 with the above in size
		self.regexed_items = []
 
		self.setWindowFlags(QC.Qt.Window)
		self.setWindowTitle('Maximum Replacer')
		self.setMinimumWidth(380)
		self.setMinimumHeight(400)
 
		self.setLayout(QW.QVBoxLayout())
		self.layout().setContentsMargins(5, 5, 5, 5)
		self.layout().setSpacing(5)
		self.layout().setAlignment(QC.Qt.AlignTop)
 
		# Selection Section
		#
		gb_selection = QW.QGroupBox()
		gb_selection.setLayout(QW.QHBoxLayout())
		gb_selection.layout().setContentsMargins(2,2,2,2)
		gb_selection.layout().setSpacing(5)
		gb_selection.setTitle('Selection')
		self.layout().addWidget(gb_selection)
		#
		self.rb_select_all = QW.QRadioButton()
		self.rb_select_all.setText('All')
		self.rb_select_all.setChecked(True)
		gb_selection.layout().addWidget(self.rb_select_all)
		#
		self.rb_select_sel = QW.QRadioButton()
		self.rb_select_sel.setText('Selected')
		gb_selection.layout().addWidget(self.rb_select_sel)
		#
		self.txt_filter_name = QW.QLineEdit()
		self.txt_filter_name.setPlaceholderText('Pattern...')
		gb_selection.layout().addWidget(self.txt_filter_name)
		#
		self.txt_filter_type = QW.QLineEdit()
		self.txt_filter_type.setPlaceholderText('Type (e.g. transform)...')
		gb_selection.layout().addWidget(self.txt_filter_type)
 
		# Expression Section
		#
		gb_expression = QW.QGroupBox()
		gb_expression.setLayout(QW.QVBoxLayout())
		gb_expression.layout().setContentsMargins(2,2,2,2)
		gb_expression.layout().setSpacing(5)
		gb_expression.setTitle('Regular Expression')
		self.layout().addWidget(gb_expression)
		#
		expr_widget = QW.QWidget()
		expr_widget.setLayout(QW.QHBoxLayout())
		expr_widget.layout().setContentsMargins(2,2,2,2)
		expr_widget.layout().setSpacing(5)
		gb_expression.layout().addWidget(expr_widget)
		#
		lbl_regex = QW.QLabel()
		lbl_regex.setText('Pattern')
		expr_widget.layout().addWidget(lbl_regex)
		#
		self.txt_replace_expr = QW.QLineEdit()
		self.txt_replace_expr.setPlaceholderText('Regex...')
		expr_widget.layout().addWidget(self.txt_replace_expr)
		#
		subs_widget = QW.QWidget()
		subs_widget.setLayout(QW.QHBoxLayout())
		subs_widget.layout().setContentsMargins(2,2,2,2)
		subs_widget.layout().setSpacing(5)
		gb_expression.layout().addWidget(subs_widget)
		#
		lbl_subst = QW.QLabel()
		lbl_subst.setText('Substitute')
		subs_widget.layout().addWidget(lbl_subst)
		#
		self.txt_replace_subs = QW.QLineEdit()
		self.txt_replace_subs.setPlaceholderText('Substitute...')
		subs_widget.layout().addWidget(self.txt_replace_subs)
 
		# Preview Section
		#
		gb_preview = QW.QGroupBox()
		gb_preview.setLayout(QW.QVBoxLayout())
		gb_preview.layout().setContentsMargins(2,2,2,2)
		gb_preview.layout().setSpacing(5)
		gb_preview.setTitle('Preview')
		self.layout().addWidget(gb_preview)
		#
		self.lv_preview = QW.QListWidget()
		gb_preview.layout().addWidget(self.lv_preview)
 
		# Button!
		self.btn_commit = QW.QPushButton()
		self.btn_commit.setText('Commit')
		self.layout().addWidget(self.btn_commit)
 
		# footer
		footer_widget = QW.QWidget()
		footer_widget.setLayout(QW.QHBoxLayout())
		footer_widget.layout().setContentsMargins(0,0,0,0)
		footer_widget.layout().setSpacing(5)
		self.layout().addWidget(footer_widget)
 
		# copyright!
		info_lbl = QW.QLabel()
		info_lbl.setTextFormat(QC.Qt.RichText)
		info_lbl.setOpenExternalLinks(True)
		info_lbl.setText('Maximum Replacer v1.2 <a href=\"http://www.dgreen.me/\">www.dgreen.me</a>')
		footer_widget.layout().addWidget(info_lbl, 0, QC.Qt.AlignLeft)
		# update while typing checkbox
		self.chk_update_while_typing = QW.QCheckBox()
		self.chk_update_while_typing.setText('Update while typing')
		self.chk_update_while_typing.setChecked(True)
		footer_widget.layout().addWidget(self.chk_update_while_typing, 0, QC.Qt.AlignRight)
 
 
		# connections
		self.txt_filter_name.textChanged.connect(self.on_text_changed)
		self.txt_filter_type.textChanged.connect(self.on_text_changed)
		self.txt_replace_expr.textChanged.connect(self.on_text_changed)
		self.txt_replace_subs.textChanged.connect(self.on_text_changed)
		self.txt_filter_name.editingFinished.connect(self.on_text_edited)
		self.txt_filter_type.editingFinished.connect(self.on_text_edited)
		self.txt_replace_expr.editingFinished.connect(self.on_text_edited)
		self.txt_replace_subs.editingFinished.connect(self.on_text_edited)
		self.rb_select_all.clicked.connect(self.update)
		self.rb_select_sel.clicked.connect(self.update)
		self.btn_commit.clicked.connect(self.commit)
 
		# initial
		self.update()
	#end
 
	# called when any text changes in text fields
	def on_text_changed(self):
		if not self.chk_update_while_typing.isChecked():
			return
 
		self.update()
	#end
 
	# called when changes have been committed in text fields (e.g. return pressed)
	def on_text_edited(self):
		if self.chk_update_while_typing.isChecked():
			return
 
		self.update()
	#end
 
	def edit_done(self):
		print 'Editing done'
	#end
 
	def get_real_short_names(self, selected):
		result = []
		for x in mc.ls(sl=selected, shortNames=True):
			result.append(x[x.rfind('|')+1:]) # basically strip all after last | (the |+1 becomes 0 if the find fails, so it's okay to fail)
		return result
	#end
 
	def get_selection(self, regex=None):
		result = []
 
		# all objects
		if self.rb_select_all.isChecked():
			result = zip(self.get_real_short_names(False), mc.ls(long=True))
 
		# selected objects
		if self.rb_select_sel.isChecked():
			result = zip(self.get_real_short_names(True), mc.ls(sl=True, long=True))
 
		# filter by type
		filter_type = self.txt_filter_type.text()
		if len(filter_type):
			to_remove = []
			for idx in range(len(result)):
				node_type = mc.nodeType(result[idx][1])
				try:
					if None == re.search(filter_type, node_type):
						to_remove.append(idx)
				except:
					continue
			#end for
 
			# remove all non-matching elements
			result = [x for idx, x in enumerate(result) if idx not in to_remove]
		#end
 
		# filter by expression
		pattern = self.txt_filter_name.text()
		if len(pattern):
			to_remove = []
			for idx in range(len(result)):
				try:
					if None == re.search(pattern, result[idx][0]):
						to_remove.append(idx)
				except:
					continue
			#end for
 
			# remove all non-matching elements
			result = [x for idx, x in enumerate(result) if idx not in to_remove]
		#end
 
		return result
	#end
 
	def calculate_regexed_names(self):
		pattern = self.txt_replace_expr.text()
		subs = self.txt_replace_subs.text()
		result = []
 
		for x in self.selected_items:
			subbed_name = x[0]
			try:
				subbed_name = re.sub(pattern, subs, x[0])
				subbed_name = mel.eval('formValidObjectName(\"{0}\");'.format(subbed_name)) # make it maya-valid
				result.append((subbed_name, subbed_name != x[0])) # (regex name, changed from original)
			except:
				result.append((subbed_name, False)) # failed so just pass through data and make it not changed
			
		return result
	#end
 
	def update(self):
		# 1. get the selection
		self.selected_items = self.get_selection()
 
		# 2. get the regex'd versions
		self.regexed_items = self.calculate_regexed_names()
 
		# 3. update list view with a preview of changes
		bold_font = QG.QFont('', -1, QG.QFont.Bold, False)
		self.lv_preview.clear()
		for x in range(len(self.selected_items)):
			short_old = self.selected_items[x][0]
			short_new = self.regexed_items[x][0]
			if self.regexed_items[x][1]:
				txt = short_old + ' => ' + short_new
			else:
				txt = short_old
			self.lv_preview.addItem(txt)
			if self.regexed_items[x][1]:
				self.lv_preview.item(self.lv_preview.count()-1).setFont(bold_font)
	#end
 
	def commit(self):
		# safety check
		if None == self.selected_items or None == self.regexed_items:
			return
 
		# confirm dialog
		number_different = len([x for x in self.regexed_items if x[1]])
		dialog_msg = 'Confirm rename of ' + str(number_different) + ' objects?'
		dialog_result = mc.confirmDialog(title='Maximum Replacer', message=dialog_msg, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
		if 'No' == dialog_result:
			return
 
		# undo chunk for all names
		mc.undoInfo(openChunk=True, chunkName='MaximumReplacer')
 
		# rename all objects (in REVERSE order as to not break the hierarchy)
		for x in reversed(range(len(self.selected_items))):
			# ignore nodes that don't need changing
			if not self.regexed_items[x][1]:
				continue
				
			old_name = self.selected_items[x][1] # old LONG name
			new_name = self.regexed_items[x][0] # new SHORT name
			
			try:
				mc.rename(old_name, new_name)
			except Exception as e:
				print 'Failed to rename %s: %s' % (old_name, e)
 
		# end chunk!
		mc.undoInfo(closeChunk=True)
 
		# refresh view
		self.update()
	#end
#end
 
def create():
	global g_maximum_replacer_inst
 
	try:
		g_maximum_replacer_inst.close()
		g_maximum_replacer_inst.deleteLater()
	except:
		pass
 
	g_maximum_replacer_inst = MaximumReplacer()
	g_maximum_replacer_inst.setAttribute(QC.Qt.WA_DeleteOnClose)
	g_maximum_replacer_inst.show()
#end

# uncomment this to run directly from the script editor (or call it from a shelf)
# create()
