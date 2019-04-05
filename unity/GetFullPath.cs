// You must put this function somewhere - Unity cannot handle standalone functions like this in files.
// Use it to retrieve the full path of any GameObject.
// originated here: https://answers.unity.com/questions/8500/how-can-i-get-the-full-path-to-a-gameobject.html?childToView=8502
//

public static string getFullPath( GameObject obj ) {
	string path = "/" + obj.name;
	while( obj.transform.parent != null ) {
		obj = obj.transform.parent.gameObject;
		path = "/" + obj.name + path;
	}
	return path;
}
