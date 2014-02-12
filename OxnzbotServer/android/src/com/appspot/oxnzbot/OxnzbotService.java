package com.appspot.oxnzbot;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

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
     * ������������������������������ 
     * public void onServiceConnected(ComponentName name, IBinder binder) 
     * IBinder I����interface��������������service����������Binder������ 
     * ��������Binder������������service������ 
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
		
		new Thread(retriveCommand).start();
		
	}
	
	Runnable retriveCommand = new Runnable() {
		private String url = "http://www.baidu.com/";
		private String result = null;
		
		@Override
		public void run() {
			try {
				HttpGet get = new HttpGet(url);
				HttpResponse resp = (new DefaultHttpClient()).execute(get);
				result = EntityUtils.toString(resp.getEntity());
				Log.d(TAG, "result=" + result);
			} catch (Exception e) {
				e.printStackTrace();
			}

			try {
				//HttpPost post = new HttpPost(url);
				//post.setEntity(httpEntity);
				//HttpClient
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	};
	
}
