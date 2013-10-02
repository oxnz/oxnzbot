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
     * true ��ʾconnectionû����һ��service�󶨣�����Ҫunbound�� 
     * false��ʾconnection�Ѿ���һ��service�󶨣���Ҫunbound<p> 
     * ���ڼ�¼mServiceConnection�Ƿ��Ѿ�unbound�ˣ�һ���Ѿ��󶨵�connection 
     * �ڳ����˳�ǰ����Ҫunbound����Ȼ����й©�����ң�unboundֻ����һ�Σ� 
     * ���unbound�ᱨ�� 
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
         * ����service�����������Ϊ����������app�˳��� 
         * ������Ȼ�����˳��� 
         */
		startService(new Intent(this, OxnzbotService.class));
		/** 
         * �󶨵�service�����serviceû����������ô�󶨵�ʱ����Զ����� 
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
         * ��activity����ǰ�жϣ����connection������ 
         * ��service����ôunbound�� 
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