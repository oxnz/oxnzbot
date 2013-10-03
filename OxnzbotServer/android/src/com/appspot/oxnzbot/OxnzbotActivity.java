package com.appspot.oxnzbot;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;

public class OxnzbotActivity extends Activity implements OnClickListener {
	private static final String TAG = "Oxnzbot activity";

	private OxnzbotService mBoundService = null;
	/** 
     * true 表示connection没有与一个service绑定，不需要unbound； 
     * false表示connection已经与一个service绑定，需要unbound<p> 
     * 用于记录mServiceConnection是否已经unbound了，一个已经绑定的connection 
     * 在程序退出前必须要unbound，不然会有泄漏。并且，unbound只能有一次， 
     * 多次unbound会报错。 
     */  
    boolean isConnectionUnbound = true;
	private ServiceConnection mServiceConnection = new ServiceConnection() {

		@Override
		public void onServiceConnected(ComponentName name, IBinder binder) {
			mBoundService = ((OxnzbotService.LocalBinder) binder).getService();
			Log.d(TAG, "onServiceConnected(), service:" + mBoundService);
		}

		@Override
		public void onServiceDisconnected(ComponentName arg0) {
			mBoundService = null;
			Log.d(TAG, "onServiceDisconnected()");
		}
		
	};
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_oxnzbot);
		
		Log.d(TAG, "oxnzbot activity created");
		/** 
         * 启动service，用这句是因为这样可以在app退出后， 
         * 服务仍然不会退出。 
         */
		startService(new Intent(this, OxnzbotService.class));
		/** 
         * 绑定到service，如果service没有启动，那么绑定的时候会自动创建 
         */  
        bindService(new Intent(this, OxnzbotService.class),   
                mServiceConnection, BIND_AUTO_CREATE);
        isConnectionUnbound = true;
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	@Override
	public void onDestroy() {
		Log.d(TAG, "onDestroy()");
		/** 
         * 在activity结束前判断，如果connection还连接 
         * 到service，那么unbound。 
         */
		if (isConnectionUnbound) {
			this.unbindService(mServiceConnection);
			isConnectionUnbound = false;
			Log.d(TAG, "unbind service");
		}
		super.onDestroy();
	}
	
	@Override
	public void onClick(View v) {
		switch (v.getId()) {
		case R.id.startButton:
			Log.d(TAG, "start button clicked");
			startService(new Intent(this, OxnzbotService.class));
			break;
		case R.id.stopButton:
			Log.d(TAG, "stop button clicked");
			if (isConnectionUnbound) {
				//this.unbindService(mServiceConnection);
				isConnectionUnbound = false;
			}
			stopService(new Intent(this, OxnzbotService.class));
			break;
		}
		
	}
}