package com.example.akshaydesai.desktoptexting;


import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
import android.util.Log;

/**
 * Created by akshaydesai on 6/23/17.
 */
public class SMSReceive extends BroadcastReceiver {
    final SmsManager sms = SmsManager.getDefault();

    public void onReceive(Context context, Intent intent){
        final Bundle bundle = intent.getExtras();
        try{
            if(bundle !=null){
                final Object[] pdusArr = (Object[]) bundle.get("pdus");

                for (int i =0; i<pdusArr.length;i++){
                    SmsMessage currentMsg = SmsMessage.createFromPdu((byte[])pdusArr[i]);
                    String currentNum = currentMsg.getDisplayOriginatingAddress();
                    String Msg = currentMsg.getDisplayMessageBody();
                    Log.d(currentNum,Msg);

                    Intent serviceIntent = new Intent(context,BackgroundReceive.class);
                    serviceIntent.putExtra("num", currentNum);
                    serviceIntent.putExtra("msg", Msg);
                    context.startService(serviceIntent);


                }
            }
        } catch (Exception e){
            Log.e("SmsReceiver", "Exception smsReceiver" +e);
            e.printStackTrace();
        }

    }

}

