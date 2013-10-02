package com.appspot.oxnzbot;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

public class OxnzbotService extends Service {
	private static final String TAG = "Retrieve Command Service";

	private IBinder mBinder = new LocalBinder();
	
	public class LocalBinder extends Binder {
		public OxnzbotService getService() {
			return OxnzbotService.this;
		}
	}
	
	/** 
     * 这个函数的返回值会当作参数传到 
     * public void onServiceConnected(ComponentName name, IBinder binder) 
     * IBinder I是指interface，一般我们会在service类实现一个Binder，这样 
     * 通过这个Binder，我们可以与service交互。 
     */ 
	@Override
	public IBinder onBind(Intent intent) {
		Log.d(TAG, "onBind");
		return mBinder;
	}
	
	@Override
	public void onCreate() {
		Toast.makeText(this, "My service created", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onCreate()");
	}

	@Override
	public void onDestroy() {
		Toast.makeText(this, "onDestroy()", Toast.LENGTH_SHORT).show();
		Log.d(TAG, "onDestroy()");
	}
	
	@Override
	public void onStart(Intent intent, int startid) {
		Toast.makeText(this, "onStart()", Toast.LENGTH_LONG).show();
		Log.d(TAG, "onStart()");
	}
}
