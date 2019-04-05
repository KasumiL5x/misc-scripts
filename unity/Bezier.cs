// Bezier.cs
// Daniel Green (and various code from the past - no idea of the original sources over time).
// 
// Create an instance of this class and use setControlPoints() to set the Bezier points.
// Use samplePoints() to calculate the final sampled array of Bezier points.
// Sampling can use a cutoff (i.e. how far along the curve to sample).
// Returned values give a BezierPointTangent which contains a position and tangent at that point.
// 
// Example:
//var points = new List<Vector3>();
//for(int i = 0; i < transform.childCount; ++i ) {
//  var child = transform.GetChild(i);
//  points.Add(child.transform.position);
//}
// 
// Bezier bezier = new Bezier();
// bezier.setControlPoints(points);
// var samples = bezier.samplePoints(10);
// 
// var bezierPositions = new List<Vector3>();
// foreach(var s in samples) {
//   bezierPositions.Add(s.point);
// }
// var line = GetComponent<LineRenderer>();
// line.positionCount = bezierPositions.Count;
// line.SetPositions(bezierPositions.ToArray());
// 

using UnityEngine;
using System;
using System.Collections.Generic;
 
public class BezierPointTangent {
	public Vector3 point;
	public Vector3 tangent;
 
	public BezierPointTangent( Vector3 p, Vector3 t ) {
		point = p;
		tangent = t;
	}
}
 
public class Bezier {
	List<Vector3> controlPoints_;
	int curveCount_ = 0;
 
 
	public void setControlPoints( List<Vector3> points ) {
		controlPoints_ = points;
		curveCount_ = controlPoints_.Count / 3;
	}
 
	public List<BezierPointTangent> samplePoints( int samplesPerSegment ) {
		List<BezierPointTangent> points = new List<BezierPointTangent>();
 
		for( int currCurve = 0; currCurve < curveCount_; ++currCurve ) {
			for( int currSeg = 0; currSeg <= samplesPerSegment; ++currSeg ) {
				float t = (0==currSeg) ? 0.0f : (float)currSeg / (float)samplesPerSegment;
 
				int index = currCurve * 3;
				var p0 = controlPoints_[index+0];
				var p1 = controlPoints_[index+1];
				var p2 = controlPoints_[index+2];
				var p3 = controlPoints_[index+3];
 
				var point = calculateBezierPoint(t, p0, p1, p2, p3);
				var tangent = calculateBezierTangent(t, p0, p1, p2, p3);
				points.Add(new BezierPointTangent(point, tangent));
			}
		}
 
		return points;
	}
 
	public List<BezierPointTangent> samplePoints( int samplesPerSegment, float cutoff ) {
		cutoff = Mathf.Clamp(cutoff, 0.0f, 1.0f);
		int totalPoints = samplesPerSegment * curveCount_;
		bool exit = false;
 
		List<BezierPointTangent> points = new List<BezierPointTangent>();
 
		for( int currCurve = 0; currCurve < curveCount_; ++currCurve ) {
			for( int currSeg = 0; currSeg <= samplesPerSegment; ++currSeg ) {
				int currPoint = (currCurve * samplesPerSegment) + currSeg;
				float percentage = (((float)currPoint * 100.0f) / (float)totalPoints) / 100.0f;
 
				float t = (0==currSeg) ? 0.0f : (float)currSeg / (float)samplesPerSegment;
 
				int index = currCurve * 3;
				var p0 = controlPoints_[index+0];
				var p1 = controlPoints_[index+1];
				var p2 = controlPoints_[index+2];
				var p3 = controlPoints_[index+3];
 
				var point = calculateBezierPoint(t, p0, p1, p2, p3);
				var tangent = calculateBezierTangent(t, p0, p1, p2, p3);
				points.Add(new BezierPointTangent(point, tangent));
 
				if( percentage >= cutoff ) {
					exit = true;
					break;
				}
			}
			if( exit ) {
				break;
			}
		}
 
		return points;
	}
 
	public float length( int steps=10 ) {
		if( steps <= 0 ) {
			throw new ArgumentException ("Steps must be positive and nonzero.", "steps");
		}
 
		float totalLength = 0.0f;
		Vector3 lastPoint = Vector3.zero;
 
		for( int currCurve = 0; currCurve < curveCount_; ++currCurve ) {
			for( int currStep = 0; currStep <= steps; ++currStep ) {
				int index = currCurve * 3;
				var p0 = controlPoints_[index+0];
				var p1 = controlPoints_[index+1];
				var p2 = controlPoints_[index+2];
				var p3 = controlPoints_[index+3];
 
				float t = (0 == currStep) ? 0.0f : (float)currStep / (float)steps;
				var point = calculateBezierPoint(t, p0, p1, p2, p3);
				if( currStep > 0 ) {
					totalLength += Vector3.Distance (point, lastPoint);
				}
				lastPoint = point;
			}
		}
 
		return totalLength;
	}
 
	Vector3 calculateBezierTangent( float t, Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3 ) {
		float nt = 1.0f - t;
		float x = -3.0f * p0.x * nt * nt  +  3.0f * p1.x * (1.0f - 4.0f * t + 3.0f * t * t)  +  3.0f * p2.x * (2.0f * t - 3.0f * t * t)  +  3.0f * p3.x * t * t;
		float y = -3.0f * p0.y * nt * nt  +  3.0f * p1.y * (1.0f - 4.0f * t + 3.0f * t * t)  +  3.0f * p2.y * (2.0f * t - 3.0f * t * t)  +  3.0f * p3.y * t * t;
		float z = -3.0f * p0.z * nt * nt  +  3.0f * p1.z * (1.0f - 4.0f * t + 3.0f * t * t)  +  3.0f * p2.z * (2.0f * t - 3.0f * t * t)  +  3.0f * p3.z * t * t;
		return new Vector3(x, y, z);
	}
 
	Vector3 calculateBezierPoint( float t, Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3 ) {
		float u = 1 - t;
		float tt = t * t;
		float uu = u * u;
		float uuu = uu * u;
		float ttt = tt * t;
		Vector3 p = uuu * p0;
		p += 3 * uu * t * p1;
		p += 3 * u * tt * p2;
		p += ttt * p3;
		return p;
	}
}