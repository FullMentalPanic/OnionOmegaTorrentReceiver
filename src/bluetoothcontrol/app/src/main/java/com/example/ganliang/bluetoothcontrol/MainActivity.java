package com.example.ganliang.bluetoothcontrol;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Handler;
import android.os.Message;
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
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
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
    BluetoothDevice btDevice = null;
    BluetoothSocket btSocket;
    int connect_state = 0;
    TextView stateTextView;
    final UUID sppUuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    List<BluetoothDevice> mArraydevice = new ArrayList<BluetoothDevice>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBluetoothAdapter == null) {
            // Device does not support Bluetooth
            Toast.makeText(MainActivity.this,
                    "Device does not support Bluetooth", Toast.LENGTH_SHORT).show();
            return;
        }else{
            if (!mBluetoothAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
        }

        Toolbar toolbar =(Toolbar) findViewById(R.id.app_bar);
        setSupportActionBar(toolbar);
        stateTextView = (TextView) findViewById(R.id.status);
        stateTextView.setText("not connect");
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
                dialog();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }


    }

    public void dialog() {
        List<String> mArrayAdapter = new ArrayList<String>();

        Set<BluetoothDevice> bondedDevices = mBluetoothAdapter.getBondedDevices();
        if (bondedDevices.size()>0){
            for (BluetoothDevice device : bondedDevices) {
                //sendLogMessage("Paired device: " + dev.getName() + " (" + dev.getAddress() + ")");
                mArrayAdapter.add(device.getName()+ " (" + device.getAddress() + ")");
                mArraydevice.add(device);
            }
        }
        else{
            Toast.makeText(MainActivity.this,
                    "no pair bluetooth", Toast.LENGTH_SHORT).show();
            return;
        }

        CharSequence[] array = new CharSequence[mArrayAdapter.size()];
        mArrayAdapter.toArray(array);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("FindDevice");
        builder.setSingleChoiceItems(array, -1, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                btDevice = mArraydevice.get(which);
            }
        });
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        if (btDevice == null){
                            Toast.makeText(MainActivity.this,
                                    "Bluetooth device is not found", Toast.LENGTH_SHORT).show();
                            return;
                        }
                        Toast.makeText(MainActivity.this,
                                "connecting", Toast.LENGTH_SHORT).show();
                        if (connect_state == 0) {
                            ConnectThread p = new ConnectThread(btDevice);
                            p.start();
                        }
                    }
                });
        builder.setNegativeButton("NO", new DialogInterface.OnClickListener(){
            public void onClick(DialogInterface dialog, int id) {
                btDevice = null;
                connect_state = 0;
                return;
            }

        });

        AlertDialog alertDialog = builder.create();
        alertDialog.show();

    }

    public class ConnectThread extends Thread{

        public ConnectThread(BluetoothDevice bTDevice){
            BluetoothSocket tmp = null;
            try {
                tmp = bTDevice.createRfcommSocketToServiceRecord(sppUuid);
            } catch (IOException e) {
                return;
            }
            btSocket = tmp;
        }

        public void run() {
            Message msg = new Message();
            try {
                btSocket.connect();
            } catch(IOException e) {
                try {
                    btSocket.close();
                } catch(IOException close) {

                    return;
                }
                mHandler.sendMessage(msg);
                return;
            }
            connect_state = 1;
            mHandler.sendMessage(msg);
        }

        public boolean cancel() {
            try {
                connect_state = 0;
                btSocket.close();
            } catch(IOException e) {
                return false;
            }
            return true;
        }
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
                if (connect_state == 1){
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("o");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        up_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("n");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        down_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("l");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        right_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("f");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        left_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("b");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        pause_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("p");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        stop_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("s");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

        close_button.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View arg0) {
                if (connect_state == 1) {
                    try {
                        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(btSocket.getOutputStream(), "ASCII"));
                        writer.write("e");
                        writer.flush();
                    } catch (IOException ex) {
                        Toast.makeText(MainActivity.this,
                                "Failed to send ", Toast.LENGTH_SHORT).show();
                    }
                }
            }
        });

    }

    private Handler mHandler = new Handler() {

        @Override
        public void handleMessage (Message msg) {
            super.handleMessage(msg);
                if (connect_state == 0){
                    stateTextView.setText("not connect");
                }
                else{
                    stateTextView.setText("connect");
                }


            }
        };

}
