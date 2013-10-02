package com.appspot.oxnzbot;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class OxnzbotBroadcastReceiver extends BroadcastReceiver {
	public static final String TAG = "OxnzbotBroadcastReceiver";
	@Override
	public void onReceive(Context context, Intent intent) {
		if (intent.equals(Intent.ACTION_BOOT_COMPLETED)) {
			Log.v(TAG, "receive ACTION_BOOT_COMPLETED");
		}
		Intent service = new Intent(context, OxnzbotService.class);
		context.startService(service);
	}
}
