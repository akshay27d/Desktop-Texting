package com.example.akshaydesai.desktoptexting;


import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.telephony.SmsManager;
import android.util.Log;

import com.jcraft.jsch.Channel;
import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Properties;
import java.util.Vector;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;

/**
 * Created by akshaydesai on 6/23/17.
 */

public class BackgroundSend extends IntentService {
    public BackgroundSend() {
        super("BackgroundSend");
    }
    @Override
    protected void onHandleIntent(Intent workIntent) {
        // Gets data from the incoming Intent
        String dataString = workIntent.getDataString();

        while(true) {
            try {
                JSch jsch = new JSch();

                Session session = jsch.getSession("user","host", 22);
                session.setPassword("password");

                // Avoid asking for key confirmation
                Properties prop = new Properties();
                prop.put("StrictHostKeyChecking", "no");
                session.setConfig(prop);

                session.connect();
                Log.d("TAG", "It's connected? " + session.isConnected());

                Context context = getApplication();

                Channel channel = session.openChannel("sftp");
                channel.connect();
                ChannelSftp sftp = (ChannelSftp) channel;

                FileOutputStream outputStream;
                SmsManager smsManager = SmsManager.getDefault();


                sftp.cd("Desktop/Desktop-Texting/outgoing/");

                        /* This opens the "outgoing"folder, copies the files over,
                            and sends it to the correct recipient */

                Vector<ChannelSftp.LsEntry> list = sftp.ls("*.txt");
                for (ChannelSftp.LsEntry entry : list) {
                    InputStream in = sftp.get(entry.getFilename());      //Getting file
                    try {
                        outputStream = openFileOutput("FileRead.txt", Context.MODE_PRIVATE);    //Writing to local
                        int c;
                        while ((c = in.read()) != -1) {
                            outputStream.write(c);
                        }
                        outputStream.close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    in.close();
                    int length = 2;
                    String arr[] = new String[length];      //Example to read file
                    arr = readFile("FileRead.txt", length);
                    Log.d("GOOD", "sdf " + arr[0] + "\n" + arr[1]);  //Print 1st 2 lines

                    ArrayList<String> parts = smsManager.divideMessage(arr[1]);
                    smsManager.sendMultipartTextMessage(arr[0], null, parts, null, null);

                    Log.d("YUP", "Got Here");
                    sftp.rm(entry.getFilename());
                }

                channel.disconnect();
                session.disconnect();

            } catch (Exception e) {
                e.printStackTrace();
                Log.d("TAG", "Didnt work");
            }
            try{
                TimeUnit.SECONDS.sleep(15);}catch(Exception e){}
        }
    }

    public String[] readFile(String name, int length){                  //read file on local system
        Context context = getApplication();
        String arr[] = new String[length];
        try {
            FileInputStream fis = context.openFileInput(name);          //Reading a File
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            String line;
            int i = 0;
            while ((line = br.readLine()) != null) {         //Converting to String array
                arr[i] = line;
                i++;
            }
            br.close();
        }catch(Exception e){
            e.printStackTrace();
        }

        return arr;
    }
}
