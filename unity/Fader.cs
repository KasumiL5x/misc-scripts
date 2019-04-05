// Fader.cs
// Daniel Green
// 
// Attach script to any GameObject and add objects you want to fade to the ObjectsToFade list in the inspector.
// Trigger fade in and out using the public fadeIn() and fadeOut() functions.
// Remember to use a material that supports transparency in its color channel!

using UnityEngine;
using System.Collections.Generic;
 
public class Fader : MonoBehaviour {
	public float FadeInTime = 1.0f; /**< Time it takes to fade in. */
	public float FadeOutTime = 1.0f; /**< Time it takes to fade out. */
	float fadeTimer_ = 0.0f; /**< Actual fade timer (counts down). */
	bool isFading_ = false; /**< Is the fade in progress? */
	bool fadingOut_ = false; /**< True if fading out, false otherwise. */
	public List<GameObject> ObjectsToFade = new List<GameObject>(); /**< Objects to fade. */
	public bool DisableOnInvisible = true; /**< Disables GameObjects when their alpha is set to zero.  Auto-enables when fading in. */
	bool firstFade_ = true; /**< Used to force first fade rules. */
 
	void Start () {
		fadeTimer_ = FadeInTime;
	}
 
	void Update () {
		if( !isFading_ ) {
			return;
		}
 
		fadeTimer_ -= Time.deltaTime;
 
		float FadeTime = fadingOut_ ? FadeOutTime : FadeInTime;
		float alpha = (FadeTime - fadeTimer_) / FadeTime;
		if( fadingOut_ ) {
			alpha = 1.0f - alpha;
		}
 
		alpha = Mathf.Clamp(alpha, 0.0f, 1.0f);
 
		if( fadeTimer_ <= 0.0f ) {
			isFading_ = false;
			fadeTimer_ = 0.0f;
			alpha = fadingOut_ ? 0.0f : 1.0f;
		}
 
		foreach( var obj in ObjectsToFade ) {
			if(null == obj) {
				Debug.Log("Object was null.");
				continue;
			}
			var renderer = obj.GetComponent<Renderer>();
			if( null == renderer ) {
				Debug.Log("Object's Renderer was null.");
				continue;
			}
			var color = renderer.material.color;
			renderer.material.color = new Color(color.r, color.g, color.b, alpha);
 
			if( DisableOnInvisible && !isFading_ && alpha <= 0.00001f ) {
				obj.SetActive(false);
			}
		}
	}
 
	public void fadeIn() {
		// if first fade, set all alpha to zero
		if( firstFade_) {
			foreach( var obj in ObjectsToFade ) {
				if(null == obj) {
					Debug.Log("Object was null.");
					continue;
				}
				var renderer = obj.GetComponent<Renderer>();
				if( null == renderer ) {
					Debug.Log("Object's Renderer was null.");
					continue;
				}
				var color = renderer.material.color;
				renderer.material.color = new Color(color.r, color.g, color.b, 0.0f);
			}
		}
 
		// ignore request to fade if fade in was last requested
		if( !firstFade_ && !fadingOut_ ) {
			return;
		}
 
		firstFade_ = false;
 
		// make all objects active just in case
		if( DisableOnInvisible ) {
			foreach( var obj in ObjectsToFade ) {
				// Debug.Log("Activating " + obj.name);
				if(null == obj) {
					Debug.Log("Object  was null.");
					continue;
				}
				obj.SetActive(true);
			}
		}
 
		// if already fading out, switch to in w/ the timer set to the reversed remainder
		if( isFading_ && fadingOut_ ) {
			isFading_ = true;
			fadingOut_ = false;
			//fadeTimer_ = FadeInTime - fadeTimer_;
			float percent = fadeTimer_ / FadeOutTime;
			fadeTimer_ = FadeInTime * (1.0f - percent);
			return;
		}
 
		isFading_ = true;
		fadingOut_ = false;
		fadeTimer_ = FadeInTime;
	}
 
	public void fadeOut() {
		// if first fade, set all alpha to 1
		if( firstFade_ ) {
			foreach( var obj in ObjectsToFade ) {
				if(null == obj) {
					Debug.Log("Object was null.");
					continue;
				}
				var renderer = obj.GetComponent<Renderer>();
				if( null == renderer ) {
					Debug.Log("Object's Renderer was null.");
					continue;
				}
				var color = renderer.material.color;
				renderer.material.color = new Color(color.r, color.g, color.b, 1.0f);
			}
		}
 
		// ignore request to fade if fade out was last requested
		if( !firstFade_ && fadingOut_ ) {
			return;
		}
 
		firstFade_ = false;
 
		// if already fading in, switch to out w/ the timer set to the reversed remainder
		if( isFading_ && !fadingOut_ ) {
			isFading_ = true;
			fadingOut_ = true;
			//fadeTimer_ = FadeOutTime - fadeTimer_;
			float percent = fadeTimer_ / FadeInTime;
			fadeTimer_ = FadeOutTime * (1.0f - percent);
			return;
		}
 
		isFading_ = true;
		fadingOut_ = true;
		fadeTimer_ = FadeOutTime;
	}
}