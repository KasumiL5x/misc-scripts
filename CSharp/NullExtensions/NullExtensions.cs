// http://www.codeproject.com/Articles/109026/Chained-null-checks-and-the-Maybe-monad
 
using System;
 
public static class NullExtensions {
 
	// Returns the value from evaluator or null if o is null.
	public static TResult With<TInput, TResult>(this TInput o, Func<TInput, TResult> evaluator) where TResult : class where TInput : class {
		return (null == o) ? null : evaluator(o);
	}
		
	// Returns the value from evaluator or failureValue if o is null.
	public static TResult Return<TInput,TResult>(this TInput o, Func<TInput, TResult> evaluator, TResult failureValue) where TInput: class {
		return (null == o) ? failureValue : evaluator(o);
	}
 
 
	// Returns o if evaluator is true, otherwise null.
	public static TInput If<TInput>(this TInput o, Func<TInput, bool> evaluator) where TInput : class {
		if( null == o ) {
			return null;
		}
		return evaluator(o) ? o : null;
	}
 
	// Returns o if evaluator is false, otherwise null.
	public static TInput Unless<TInput>(this TInput o, Func<TInput, bool> evaluator) where TInput : class {
		if( null == o ) {
			return null;
		}
		return evaluator(o) ? null : o;
	}
 
	// Returns null if o is null, or otherwise runs the action delegate on o before returning o.
	public static TInput Do<TInput>(this TInput o, Action<TInput> action) where TInput: class {
		if( null == o ) {
			return null;
		}
		action(o);
		return o;
	}
}
