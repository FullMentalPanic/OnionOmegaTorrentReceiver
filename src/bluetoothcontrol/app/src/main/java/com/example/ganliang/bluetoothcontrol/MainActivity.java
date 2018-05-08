package com.example.ganliang.bluetoothcontrol;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.view.View.OnClickListener;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    ImageButton ok_button;
    ImageButton up_button;
    ImageButton down_button;
    ImageButton left_button;
    ImageButton right_button;
    ImageButton stop_button;
    ImageButton pause_button;
    ImageButton close_button;
    BluetoothAdapter mBluetoothAdapter;
    private final static int REQUEST_ENABLE_BT = 1;
    ArrayList<String> mArrayAdapter;
    ArrayList<BluetoothDevice> mArraydevice;
    BluetoothDevice btDevice = null;
    BluetoothSocket btSocket;
    final UUID sppUuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar =(Toolbar) findViewById(R.id.app_bar);
        setSupportActionBar(toolbar);
        add_Button();

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case R.id.action_settings:
                mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
                if (mBluetoothAdapter == null) {
                    // Device does not support Bluetooth
                    Toast.makeText(MainActivity.this,
                            "Device does not support Bluetooth", Toast.LENGTH_SHORT).show();
                    return super.onOptionsItemSelected(item);
                }else{
                    if (!mBluetoothAdapter.isEnabled()) {
                        Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                        startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
                    }


                }

                dialog();
                if (btDevice == null){
                    Toast.makeText(MainActivity.this,
                            "Bluetooth device is not found", Toast.LENGTH_SHORT).show();
                    return super.onOptionsItemSelected(item);
                }
                else{
                    try {
                        btSocket = btDevice.createRfcommSocketToServiceRecord(sppUuid);
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to create RfComm socket", Toast.LENGTH_SHORT).show();
                        return super.onOptionsItemSelected(item);
                    }

                    for (int i = 0; ; i++) {
                        try {
                            btSocket.connect();
                        } catch (IOException ex) {
                            if (i < 5) {
                                Toast.makeText(MainActivity.this,
                                        "Failed to connect. Retrying", Toast.LENGTH_SHORT).show();
                                continue;
                            }

                            Toast.makeText(MainActivity.this,
                                    "Failed to connect", Toast.LENGTH_SHORT).show();
                            return super.onOptionsItemSelected(item);
                        }
                        break;
                    }

                }
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }


    }


    public void dialog() {

        Set<BluetoothDevice> bondedDevices = mBluetoothAdapter.getBondedDevices();
        for (BluetoothDevice device : bondedDevices) {
            //sendLogMessage("Paired device: " + dev.getName() + " (" + dev.getAddress() + ")");
            mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
            mArraydevice.add(device);
        }
        String[] array = mArrayAdapter.toArray(new String[0]);
        new AlertDialog.Builder(this)
                .setTitle("FindDevice")
                .setItems( array, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        btDevice = mArraydevice.get(which);

                    }
                }).create().show();
    }

    public void add_Button(){
        ok_button = (ImageButton) findViewById(R.id.ok);
        up_button = (ImageButton) findViewById(R.id.up);
        down_button = (ImageButton) findViewById(R.id.down);
        left_button = (ImageButton) findViewById(R.id.left);
        right_button = (ImageButton) findViewById(R.id.right);
        stop_button = (ImageButton) findViewById(R.id.stop);
        close_button = (ImageButton) findViewById(R.id.close);
        pause_button = (ImageButton) findViewById(R.id.pause);

        ok_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("o");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        up_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("n");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        down_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("l");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        right_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("f");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        left_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("b");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        pause_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("p");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        stop_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("s");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

        close_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {

                try {
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                    writer.write("e");
                    writer.flush();
                } catch (IOException ex) {
                    Toast.makeText(MainActivity.this,
                            "Failed to send ", Toast.LENGTH_SHORT).show();
                }

            }

        });

    }


}
