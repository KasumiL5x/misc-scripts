import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
import maya.cmds as mc
import re

g_dialog = None

class ValueChecker(QtWidgets.QDialog):
	def __init__(self):
		QtWidgets.QDialog.__init__(self)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle('Value Checker')
		self.setFixedHeight(400)
		self.setFixedWidth(370)

		self.setLayout(QtWidgets.QVBoxLayout())
		self.layout().setContentsMargins(5, 5, 5, 5)
		self.layout().setSpacing(5)

		# naming pattern section
		#
		# group box
		pattern_gb = QtWidgets.QGroupBox()
		pattern_gb.setTitle('Naming Pattern')
		pattern_gb.setLayout(QtWidgets.QVBoxLayout())
		pattern_gb.setFixedHeight(150)
		pattern_gb.layout().setContentsMargins(5, 5, 5, 5)
		pattern_gb.layout().setSpacing(5)
		self.layout().addWidget(pattern_gb)
		# textbox container
		pattern_tb_widget = QtWidgets.QWidget()
		pattern_tb_widget.setLayout(QtWidgets.QHBoxLayout())
		pattern_tb_widget.layout().setContentsMargins(0, 0, 0, 0)
		pattern_tb_widget.layout().setSpacing(0)
		pattern_gb.layout().addWidget(pattern_tb_widget)
		# pattern textbox
		self.pattern_name_tb = QtWidgets.QLineEdit()
		self.pattern_name_tb.setPlaceholderText('Filter by name...')
		pattern_tb_widget.layout().addWidget(self.pattern_name_tb)
		# type textbox
		self.pattern_type_tb = QtWidgets.QLineEdit()
		self.pattern_type_tb.setPlaceholderText('Filter by type (e.g. transform)...')
		pattern_tb_widget.layout().addWidget(self.pattern_type_tb)
		# pattern preview
		self.pattern_lb = QtWidgets.QListWidget()
		self.pattern_lb.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		pattern_gb.layout().addWidget(self.pattern_lb)

		# validation section
		#
		# group box
		validation_gb = QtWidgets.QGroupBox()
		validation_gb.setTitle('Validation')
		validation_gb.setLayout(QtWidgets.QVBoxLayout())
		validation_gb.layout().setContentsMargins(5, 5, 5, 5)
		validation_gb.layout().setSpacing(5)
		self.layout().addWidget(validation_gb)
		# attribute section
		validation_attribs_widget = QtWidgets.QWidget()
		validation_attribs_widget.setLayout(QtWidgets.QHBoxLayout())
		validation_attribs_widget.layout().setContentsMargins(0, 0, 0, 0)
		validation_attribs_widget.layout().setSpacing(5)
		validation_gb.layout().addWidget(validation_attribs_widget)
		# attribute combobox
		self.validation_attribs_combobox = QtWidgets.QComboBox()
		self.validation_attribs_combobox.setFixedWidth(150)
		self.validation_attribs_combobox.setEditable(True)
		validation_attribs_widget.layout().addWidget(self.validation_attribs_combobox)
		# should be combobox
		self.validation_attribs_shouldbe = QtWidgets.QComboBox()
		self.validation_attribs_shouldbe.setFixedWidth(60)
		self.validation_attribs_shouldbe.addItem('==')
		self.validation_attribs_shouldbe.addItem('!=')
		self.validation_attribs_shouldbe.addItem('<')
		self.validation_attribs_shouldbe.addItem('<=')
		self.validation_attribs_shouldbe.addItem('>')
		self.validation_attribs_shouldbe.addItem('>=')
		validation_attribs_widget.layout().addWidget(self.validation_attribs_shouldbe)
		# value textbox
		self.validation_attribs_value = QtWidgets.QLineEdit()
		self.validation_attribs_value.setPlaceholderText('value')
		validation_attribs_widget.layout().addWidget(self.validation_attribs_value)
		# checkbox section
		validation_chk_widget = QtWidgets.QWidget()
		validation_chk_widget.setLayout(QtWidgets.QHBoxLayout())
		validation_chk_widget.layout().setContentsMargins(2, 0, 2, 0)
		validation_chk_widget.layout().setSpacing(0)
		validation_chk_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		validation_gb.layout().addWidget(validation_chk_widget)
		# translate checkbox
		self.validation_chk_translate = QtWidgets.QCheckBox()
		self.validation_chk_translate.setText('Zero Translation')
		validation_chk_widget.layout().addWidget(self.validation_chk_translate)
		validation_chk_widget.layout().addStretch()
		# rotate checkbox
		self.validation_chk_rotate = QtWidgets.QCheckBox()
		self.validation_chk_rotate.setText('Zero Rotation')
		validation_chk_widget.layout().addWidget(self.validation_chk_rotate)
		validation_chk_widget.layout().addStretch()
		# scale checkbox
		self.validation_chk_scale = QtWidgets.QCheckBox()
		self.validation_chk_scale.setText('Unit Scale')
		validation_chk_widget.layout().addWidget(self.validation_chk_scale)

		# validate button
		#
		self.validate_btn = QtWidgets.QPushButton()
		self.validate_btn.setText('Validate')
		self.layout().addWidget(self.validate_btn)

		# output box
		#
		self.output_tb = QtWidgets.QTextEdit()
		self.output_tb.setFixedHeight(120)
		self.output_tb.setReadOnly(True)
		self.output_tb.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)
		self.output_tb.setWordWrapMode(QtGui.QTextOption.NoWrap)
		self.layout().addWidget(self.output_tb)

		# version lbl
		#
		version_lbl = QtWidgets.QLabel()
		version_lbl.setTextFormat(QtCore.Qt.RichText)
		version_lbl.setOpenExternalLinks(True)
		version_lbl.setText('<a href=\"https://www.dgreen.me\">www.dgreen.me</a>')
		self.layout().addWidget(version_lbl)

		# connections
		self.pattern_name_tb.textChanged.connect(self.on_pattern_name_changed)
		self.pattern_type_tb.textChanged.connect(self.on_pattern_type_changed)
		self.pattern_lb.itemSelectionChanged.connect(self.update_attribs_combobox)
		self.validate_btn.clicked.connect(self.on_validate_clicked)

		# initially populate the list
		self.update_filtered_objects(self.pattern_name_tb.text(), self.pattern_type_tb.text())
	#end

	def output_error(self, msg):
		self.output_tb.setText(self.output_tb.toPlainText() + msg + '\n')
		# self.output_tb.verticalScrollBar().setValue(self.output_tb.verticalScrollBar().maximum())
	#end

	def output_mismatch_value(self, node, attrib, operator, expected, actual):
		msg = '%s.%s should be %s %s but is %s.' % (node, attrib, operator, expected, actual)
		self.output_tb.setText(self.output_tb.toPlainText() + msg + '\n')
	#end

	def on_validate_clicked(self):
		self.output_tb.clear()

		objects = self.get_filtered_objects()
		if not len(objects):
			return

		# check translate
		if self.validation_chk_translate.isChecked():
			self.output_error('Checking translations...')
			error_count = 0
			for curr_obj in objects:
				if not mc.attributeQuery('translate', node=curr_obj, ex=True):
					continue
				for c in ['tx', 'ty', 'tz']:
					value = mc.getAttr(curr_obj + '.' + c)
					if not self.are_equal(0.0, value):
						self.output_mismatch_value(curr_obj, c, '', 0.0, value)
						error_count += 1
			self.output_error('Done (%s errors).\n' % error_count)
		#end

		# check rotate
		if self.validation_chk_rotate.isChecked():
			self.output_error('Checking rotations...')
			error_count = 0
			for curr_obj in objects:
				if not mc.attributeQuery('rotate', node=curr_obj, ex=True):
					continue
				for c in ['rx', 'ry', 'rz']:
					value = mc.getAttr(curr_obj + '.' + c)
					if not self.are_equal(0.0, value):
						self.output_mismatch_value(curr_obj, c, '', 0.0, value)
						error_count += 1
			self.output_error('Done (%s errors).\n' % error_count)
		#end

		# check scale
		if self.validation_chk_scale.isChecked():
			self.output_error('Checking scales...')
			error_count = 0
			for curr_obj in objects:
				if not mc.attributeQuery('scale', node=curr_obj, ex=True):
					continue
				for c in ['sx', 'sy', 'sz']:
					value = mc.getAttr(curr_obj + '.' + c)
					if not self.are_equal(1.0, value):
						self.output_mismatch_value(curr_obj, c, '', 1.0, value)
						error_count += 1
			self.output_error('Done (%s errors).\n' % error_count)
		#end

		# get current attribute from the GUI
		attrib = self.get_current_attrib()
		if not len(attrib):
			return

		# get user-provided expected value
		expected_value = self.validation_attribs_value.text()
		if not len(expected_value):
			return

		self.output_error('Checking custom attributes...')
		error_count = 0

		# which operation are we doing?
		compare_func = None
		if self.validation_attribs_shouldbe.currentText() == '==':
			compare_func = self.are_equal
		elif self.validation_attribs_shouldbe.currentText() == '!=':
			compare_func = self.are_not_equal
		elif self.validation_attribs_shouldbe.currentText() == '<':
			compare_func = self.is_less
		elif self.validation_attribs_shouldbe.currentText() == '<=':
			compare_func = self.is_lequal
		elif self.validation_attribs_shouldbe.currentText() == '>':
			compare_func = self.is_greater
		elif self.validation_attribs_shouldbe.currentText() == '>=':
			compare_func = self.is_grequal
		else:
			self.output_error('An invalid comparison was selected.')
			return

		for curr_obj in objects:
			# object could be deleted
			if not mc.objExists(curr_obj):
				continue

			# attribute may not exist
			if not mc.attributeQuery(attrib, node=curr_obj, ex=True):
				self.output_error('Attribute not found: %s.%s.' % (curr_obj, attrib))
				continue
			
			# raw attribute value from maya
			attrib_value = mc.getAttr(curr_obj + '.' + attrib)

			comparison_succeeded = False
			if isinstance(attrib_value, bool): # MUST check bool before int because True/False passes isinstance(x, int) too.
				comparison_succeeded = compare_func(attrib_value, self.string_to_bool(expected_value))
			elif isinstance(attrib_value, int):
				try:
					expected_value_int = int(expected_value)
					comparison_succeeded = compare_func(attrib_value, expected_value_int)
				except:
					self.output_error('%s is an int; your value should be too.' % (curr_obj + '.' + attrib))
					continue
			elif isinstance(attrib_value, float):
				try:
					expected_value_float = float(expected_value)
					comparison_succeeded = compare_func(attrib_value, expected_value_float)
				except Exception as ex:
					print ex.message
					self.output_error('%s is a float; your value should be too.' % (curr_obj + '.' + attrib))
					continue


			# output mismatch notifications
			if not comparison_succeeded:
				# mini-hack: convert string to bool here if necessary to show True/False instead of 0/1/t/f/etc.
				self.output_mismatch_value(curr_obj, attrib, self.validation_attribs_shouldbe.currentText(), self.string_to_bool(expected_value) if isinstance(attrib_value, bool) else expected_value, attrib_value)
				error_count += 1

		self.output_error('Done (%s errors).' % error_count)
	#end

	def are_types_equal(self, a, b):
		return type(a) == type(b)
	#end

	def are_equal(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'are_equal\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False

		if isinstance(a, int):
			return a == b

		if isinstance(a, float):
			return abs(b - a) < 0.000001 # epsilon

		if isinstance(a, bool):
			return a == b

		self.output_error('Type not covered in \'are_equal\' (%s)! Returning False.' % type(a))
		return False
	#end

	def are_not_equal(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'are_not_equal\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False

		if isinstance(a, int):
			return not (a == b)

		if isinstance(a, float):
			return not (abs(b - a) < 0.000001) # epsilon

		if isinstance(a, bool):
			return not (a == b)

		self.output_error('Type not covered in \'are_not_equal\' (%s)! Returning False.' % type(a))
		return False
	#end
	
	def is_less(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'is_less\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False
		
		if isinstance(a, int):
			return a < b

		if isinstance(a, float):
			return a < b

		if isinstance(a, bool):
			return False # bools are either equal or not equal

		self.output_error('Type not covered in \'is_less\' (%s)! Returning False.' % type(a))
		return False
	#end

	def is_lequal(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'is_lequal\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False
		
		if isinstance(a, int):
			return a <= b

		if isinstance(a, float):
			return a < b or self.are_equal(a, b)

		if isinstance(a, bool):
			return a == b # can only check equality

		self.output_error('Type not covered in \'is_lequal\' (%s)! Returning False.' % type(a))
		return False
	#end

	def is_greater(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'is_greater\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False
		
		if isinstance(a, int):
			return a > b

		if isinstance(a, float):
			return a > b

		if isinstance(a, bool):
			return False # bools are either equal or not equal

		self.output_error('Type not covered in \'is_greater\' (%s)! Returning False.' % type(a))
		return False
	#end

	def is_grequal(self, a, b):
		if not self.are_types_equal(a, b):
			self.output_error('Type mismatch in \'is_grequal\' (%s, %s)! Returning False.' % (type(a), type(b)))
			return False
		
		if isinstance(a, int):
			return a >= b

		if isinstance(a, float):
			return a > b or self.are_equal(a, b)

		if isinstance(a, bool):
			return a == b # can only check equality

		self.output_error('Type not covered in \'is_grequal\' (%s)! Returning False.' % type(a))
		return False
	#end

	def string_to_bool(self, string):
		return string.lower() in ['true', 't', 'yes', 'y', '1']
	#end

	def get_current_attrib(self):
		return str(self.validation_attribs_combobox.currentText())
	#end

	def update_attribs_combobox(self):
		self.validation_attribs_combobox.clear()

		all_attribs = set()
		for curr_obj in self.get_filtered_objects():
			obj_attributes = mc.listAttr(curr_obj, s=True) # only scalars (includes booleans and integer-based enums)
			if None == obj_attributes:
				continue
			all_attribs = all_attribs | set(obj_attributes)
		all_attribs = sorted(all_attribs)
		
		for curr in all_attribs:
			self.validation_attribs_combobox.addItem(curr)
	#end

	def get_filtered_objects(self):
		result = []

		nothing_selected = (0 == len(self.pattern_lb.selectedItems()))

		for idx in range(self.pattern_lb.count()):
			item = self.pattern_lb.item(idx)
			if nothing_selected or item.isSelected():
				result.append(item.text())

		return result
	#end

	def update_filtered_objects(self, name_filter, type_filter):
		self.pattern_lb.clear()
		
		to_add = []
		for curr in mc.ls():
			node_name = curr
			node_type = mc.nodeType(curr)

			# if len(name_filter) and name_filter not in node_name:
			if len(name_filter) and re.search(name_filter, node_name) is None:
				continue

			# if len(type_filter) and type_filter not in node_type:
			if len(type_filter) and re.search(type_filter, node_type) is None:
				continue

			to_add.append(curr)
		#end

		for curr in to_add:
			self.pattern_lb.addItem(curr)

		self.update_attribs_combobox()
	#end

	def on_pattern_name_changed(self):
		self.update_filtered_objects(self.pattern_name_tb.text(), self.pattern_type_tb.text())
	#end

	def on_pattern_type_changed(self):
		self.update_filtered_objects(self.pattern_name_tb.text(), self.pattern_type_tb.text())
	#end
#end

def create():
	global g_dialog

	try:
		g_dialog.close()
		g_dialog.deleteLater()
	except:
		pass
	g_dialog = ValueChecker()
	g_dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
	g_dialog.show()
#end
