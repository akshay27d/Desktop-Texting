package com.example.akshaydesai.desktoptexting;


import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.FileOutputStream;
import java.util.Properties;

/**
 * Created by akshaydesai on 6/24/17.
 */

public class BackgroundReceive extends IntentService {
    protected int sentCount =-1;
    public BackgroundReceive() {
        super("BackgroundReceive");
    }

    @Override
    protected void onHandleIntent(Intent workIntent) {
        // Gets data from the incoming Intent
        String dataString = workIntent.getDataString();
        Bundle extras = workIntent.getExtras();

        String Info = (String) extras.get("num");
        String Info2 = (String) extras.get("msg");


        try {
            JSch jsch = new JSch();

            Session session = jsch.getSession(--user--,--host--, 22);
            session.setPassword(--password--);

            // Avoid asking for key confirmation
            Properties prop = new Properties();
            prop.put("StrictHostKeyChecking", "no");
            session.setConfig(prop);

            session.connect();
            Log.d("TAG", "It's connected 2? " + session.isConnected());

            Channel channel = session.openChannel("sftp");
            channel.connect();
            ChannelSftp sftp = (ChannelSftp) channel;

            Context context = getApplication();

            sentCount++;
            createFile(Integer.toString(sentCount) + ".txt", Info+"\n"+Info2, context);
            sftp.put(context.getFilesDir() + "/" +Integer.toString(sentCount) + ".txt", "Desktop/Desktop-Texting/incoming/"+Integer.toString(sentCount) + ".txt");



            channel.disconnect();
            session.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
            Log.d("TAG", "Didnt work 2");
        }
    }

    public void createFile(String name, String contents, Context context){          //Creates a file with contents
        FileOutputStream os;

        try {
            os = context.openFileOutput(name, Context.MODE_PRIVATE);
            os.write(contents.getBytes());
            os.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
