package com.appspot.oxnzbot;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;

public class OxnzbotActivity extends Activity implements OnClickListener {
	private static final String TAG = "Oxnzbot activity";

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_oxnzbot);
		Log.v(TAG, "oxnzbot activity created");
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
			stopService(new Intent(this, OxnzbotService.class));
			break;
		}
		
	}
}