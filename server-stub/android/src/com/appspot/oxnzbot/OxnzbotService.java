package com.appspot.oxnzbot;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

public class OxnzbotService extends Service {
	private static final String TAG = "Retrieve Command Service";

	@Override
	public IBinder onBind(Intent intent) {
		return null;
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
