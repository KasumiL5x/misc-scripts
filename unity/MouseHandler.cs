// MouseHandler.cs
// Daniel Green

// Use when you want to have a single static check for mouse up/hold/down.
// Attach to a GameObject so that it can update.
// In any other script, use the *static* functions addMouseDown/Hold/Up() to set callbacks.
// Look at getObjectUnderCursor() to change between 2D/3D, change direction, position, etc.

using UnityEngine;
using System.Collections.Generic;
 
public class MouseHandler : MonoBehaviour {
	public delegate void OnMouseDown( GameObject hit );
	public delegate void OnMouseHold( GameObject hit );
	public delegate void OnMouseUp( GameObject hit );
 
	static List<OnMouseDown> MouseDown = new List<OnMouseDown>();
	static List<OnMouseHold> MouseHold = new List<OnMouseHold>();
	static List<OnMouseUp> MouseUp = new List<OnMouseUp>();
 
	public Camera camera_ = null;
	bool wasMouseDown_ = false;
 
	public static void addMouseDown( OnMouseDown cb ) {
		MouseDown.Add(cb);
	}
 
	public static void addMouseHold( OnMouseHold cb ) {
		MouseHold.Add(cb);
	}
 
	public static void addMouseUp( OnMouseUp cb ) {
		MouseUp.Add(cb);
	}
 
	void Awake() {
		if( null == camera_ ) {
			Debug.Log("Camera is null.");
		}
	}
 
	void Update () {
		bool isMouseDown = Input.GetMouseButton(0);
 
		if( isMouseDown && !wasMouseDown_ ) {
			var obj = getObjectUnderCursor();
			foreach( var cb in MouseDown ) {
				cb.Invoke(obj);
			}
		} else if( isMouseDown && wasMouseDown_ ) {
			var obj = getObjectUnderCursor();
			foreach( var cb in MouseHold ) {
				cb.Invoke(obj);
			}
		} else if( !isMouseDown && wasMouseDown_ ) {
			var obj = getObjectUnderCursor();
			foreach( var cb in MouseUp ) {
				cb.Invoke(obj);
			}
		}
 
		wasMouseDown_ = isMouseDown;
	}
 
	GameObject getObjectUnderCursor() {
		// 2D:
		// var hit = Physics2D.Raycast(camera_.ScreenToWorldPoint(Input.mousePosition), Vector2.zero);
		// return (null == hit.transform) ? null : hit.transform.gameObject;

		// 3D:
		var hit = new RaycastHit();
		if(Physics.Raycast(camera_.ScreenPointToRay(Input.mousePosition), out hit)) {
			return (null == hit.transform) ? null : hit.transform.gameObject;
		}
		return null;
	}
}