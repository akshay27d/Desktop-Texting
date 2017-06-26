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

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.util.Properties;
import java.io.FileNotFoundException;

/**
 * Created by akshaydesai on 6/24/17.
 */

public class BackgroundReceive extends IntentService {
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

            int outCount=getCounterNum();
            createFile(Integer.toString(outCount) + ".txt", Info+"\n"+Info2, context);
            sftp.put(context.getFilesDir() + "/" +Integer.toString(outCount) + ".txt", "Desktop/Desktop-Texting/incoming/"+Integer.toString(outCount) + ".txt");



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

    public int getCounterNum(){
        Context context = getApplication();
        String arr[] = new String[1];
        int outCount;

        try {
            FileInputStream fis = context.openFileInput("counter.txt");          //Reading a File
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            String line;
            int i = 0;
            while ((line = br.readLine()) != null) {         //Converting to String array
                arr[i] = line;
                i++;
            }
            br.close();
            outCount = Integer.parseInt(arr[0]);
        }catch(Exception e){
            createFile("counter.txt","1", context);
            outCount=0;
        }
        createFile("counter.txt",Integer.toString(outCount+1), context);

        return outCount;
    }
}
