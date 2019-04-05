// BezierGenerator.cs
// Daniel Green (plus some online code - honestly cannot recall the origin, sorry!).
// 
// Given a set of 2D knots (points), generates control handles that, when combined with the original knots,
// ensures a Bezier curve goes directly through each knot.
// 
// Pass in an array of 2D points; these are the points the curve will go through.
// For each input point, there is a corresponding control point in each of the two
// returned lists at the same index (i.e. input point 9 has control points also at index 9)
// Combine the returned control point lists with the original input points and put them through
// a regular Bezier class to have the curve go through the given points exactly.
// 
// This implementation is in 2D.  To make it 3D, replace Vector2 with Vector3 and add the extra
// derivatives for the Z coordinate (where you see X and Y handled, add code for Z).

using UnityEngine;
using System;
using System.Collections.Generic;
 
public class BezierGenerator : MonoBehaviour {
	public static void getCurveControlPoints( List<Vector2> knots, ref List<Vector2> outFirstCPs, ref List<Vector2> outSecondCPs ) {
		if( null == knots ) {
			throw new ArgumentNullException("knots");
		}
 
		int length = knots.Count-1;
		if( length < 1 ) {
			throw new ArgumentException("At least two knot points required", "knots");
		}
 
		if( 1 == length ) { // special case: bezier curve should be a straight line
			// 3P1 = 2P0 + P3
			float firstX = (2.0f * knots[0].x + knots[1].x) / 3.0f;
			float firstY = (2.0f * knots[0].y + knots[1].y) / 3.0f;
			outFirstCPs.Add(new Vector2(firstX, firstY));
 
			// P2 = 2P1 - P0
			float secondX = 2.0f * outFirstCPs[0].x - knots[0].x;
			float secondY = 2.0f * outFirstCPs[0].y - knots[0].y;
			outSecondCPs.Add(new Vector2(secondX, secondY));
			return;
		}
 
		// calculate first bezier control points
		//
		// right hand side vector
		float[] rhs = new float[length];
		// set right hand side x values
		for( int i = 1; i < length-1; ++i ) {
			rhs[i] = 4.0f * knots[i].x + 2.0f * knots[i+1].x;
		}
		rhs[0] = knots[0].x + 2.0f * knots[1].x;
		rhs[length-1] = (8.0f * knots[length-1].x + knots[length].x) / 2.0f;
		// get first control points x values
		float[] x = getFirstControlPoints(rhs);
 
		// set right hand side y valus
		for( int i = 1; i < length-1; ++i ) {
			rhs[i] = 4.0f * knots[i].y + 2.0f * knots[i+1].y;
		}
		rhs[0] = knots[0].y + 2.0f * knots[1].y;
		rhs[length-1] = (8.0f * knots[length-1].y + knots[length].y) / 2.0f;
		float[] y = getFirstControlPoints(rhs);
 
		// fill output arrays
		outFirstCPs = new List<Vector2>();
		outSecondCPs = new List<Vector2>();
		for( int i = 0; i < length; ++i ) {
			outFirstCPs.Add(new Vector2(x[i], y[i]));
 
			float secondX;
			float secondY;
			if( i < length-1 ) {
				secondX = 2.0f * knots[i + 1].x - x[i + 1];
				secondY = 2.0f * knots[i + 1].y - y[i + 1];
			} else {
				secondX = (knots[length].x + x[length - 1]) / 2.0f;
				secondY = (knots[length].y + y[length - 1]) / 2.0f;
			}
			outSecondCPs.Add(new Vector2(secondX, secondY));
		}
	}
 
	private static float[] getFirstControlPoints( float[] rhs ) {
		int length = rhs.Length;
		float[] x = new float[length]; // solution
		float[] tmp = new float[length]; // workspace
 
		float b = 2.0f;
		x[0] = rhs[0] / b;
		for( int i = 1; i < length; ++i ) { // decomposition and forward substitution
			tmp[i] = 1.0f / b;
			b = (i < length-1 ? 4.0f : 3.5f) - tmp[i];
			x[i] = (rhs[i] - x[i-1]) / b;
		}
		for( int i = 1; i < length; ++i ) {
			x[length-i-1] -= tmp[length-i] * x[length-i]; // back substitution
		}
		return x;
	}
}