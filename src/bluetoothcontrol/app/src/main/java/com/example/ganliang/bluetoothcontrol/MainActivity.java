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
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import static android.support.v4.app.ActivityCompat.startActivityForResult;


public class MainActivity extends AppCompatActivity {

    public static final int STATE_NONE = 0;
    public static final int CONNECT_DEVICE_FAIL = 1;       // we're doing nothing
    public static final int CONNECT_FAIL = 2;       // we're doing nothing
    public static final int SOCKET_NOT_CREATED = 3;     //
    public static final int STATE_CONNECTED = 4;  // now connected to a remote device
    public static final int WRITE_IO_ERROR = 5;  // now connected to a remote device

    ImageButton ok_button;
    ImageButton up_button;
    ImageButton down_button;
    ImageButton left_button;
    ImageButton right_button;
    ImageButton stop_button;
    ImageButton pause_button;
    ImageButton close_button;
    BluetoothSerialService Blue = new BluetoothSerialService();
    TextView stateTextView;
    int ID;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Toolbar toolbar =(Toolbar) findViewById(R.id.app_bar);
        setSupportActionBar(toolbar);
        stateTextView = (TextView) findViewById(R.id.status);
        stateTextView.setText("disconnect");
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
            case R.id.action_connect:
                dialog();
                return true;
            case R.id.action_disconnect:
                Blue.disconnect();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    public void dialog() {

        AlertDialog.Builder builder = new AlertDialog.Builder(this);

        builder.setTitle("FindDevice");

        builder.setSingleChoiceItems(Blue.scan_pair_device(), -1, new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                ID = which;
            }
        });
        builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int id) {
                        BluetoothDevice Device;
                        Device = Blue.mArraydevice.get(ID);
                        if (Device == null){
                            Toast.makeText(MainActivity.this,
                                    "Bluetooth device is not found", Toast.LENGTH_SHORT).show();
                            return;
                        }
                            Toast.makeText(MainActivity.this,
                                    "connecting", Toast.LENGTH_SHORT).show();
                            Blue.connect(Device);
                        }
                });
        builder.setNegativeButton("NO", new DialogInterface.OnClickListener(){
            public void onClick(DialogInterface dialog, int id) {
                return;
            }

        });

        AlertDialog alertDialog = builder.create();
        alertDialog.show();

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
                byte[] buff = {'o', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

        up_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'n', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

        down_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'l', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

        right_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'f', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

        left_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'b', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

        pause_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'p', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }
            }
        });

        stop_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'s', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }
            }
        });

        close_button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                byte[] buff = {'e', '\n'};
                if(Blue.connectedTd != null){
                    Blue.connectedTd.write(buff);
                }

            }
        });

    }

    public class BluetoothSerialService{
        BluetoothAdapter mBluetoothAdapter;
        private final static int REQUEST_ENABLE_BT = 1;
        final UUID sppUuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
        List<BluetoothDevice> mArraydevice = new ArrayList<BluetoothDevice>();
        int status = STATE_CONNECTED;
        ConnectThread  connectTd = null;
        ConnectedThread  connectedTd = null;

        public  BluetoothSerialService(){
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
        }

        public  CharSequence[] scan_pair_device(){
            List<String> mArrayAdapter = new ArrayList<String>();
            mArraydevice.clear();
            Set<BluetoothDevice> bondedDevices = mBluetoothAdapter.getBondedDevices();
            if (bondedDevices.size()>0){
                for (BluetoothDevice device : bondedDevices) {
                    mArrayAdapter.add(device.getName()+ " (" + device.getAddress() + ")");
                    mArraydevice.add(device);
                }
            }
            else{
                Toast.makeText(MainActivity.this,
                        "no pair bluetooth", Toast.LENGTH_SHORT).show();
                return null;
            }

            CharSequence[] array = new CharSequence[mArrayAdapter.size()];
            mArrayAdapter.toArray(array);
            return array;

        }

        public void connect(BluetoothDevice Device){
            if(connectTd == null){
                connectTd =  new ConnectThread(Device);
                connectTd.start();

            }
            else{
                    connectTd.cancel();
                    connectTd = null;
                    connectTd =  new ConnectThread(Device);
                    connectTd.start();
            }
        }

        public class ConnectThread extends Thread{
            private final BluetoothDevice btDevice;
            private BluetoothSocket btSocket = null;

            public ConnectThread(BluetoothDevice Device){
                btDevice = Device;
                BluetoothSocket tmp;
                Message msg = new Message();

                try {
                    tmp = btDevice.createInsecureRfcommSocketToServiceRecord(sppUuid);//RfcommSocketToServiceRecord(sppUuid);
                } catch (IOException e) {
                    msg.what =CONNECT_DEVICE_FAIL ;
                    mHandler.sendMessage(msg);
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
                    msg.what =CONNECT_FAIL ;
                    mHandler.sendMessage(msg);
                    return;
                }

                if (connectedTd == null){
                    connectedTd = new ConnectedThread(btSocket);
                }
                else{
                    connectedTd.cancel();
                    connectedTd = null;
                    connectedTd = new ConnectedThread(btSocket);
                }

            }

            public boolean cancel() {
                try {
                    btSocket.close();
                } catch(IOException e) {
                    return false;
                }
                return true;
            }
        }
        public class ConnectedThread extends Thread{
            private BluetoothSocket mmSocket;
            private InputStream mmInStream;
            private OutputStream mmOutStream;
            public ConnectedThread(BluetoothSocket socket) {
                mmSocket = socket;
                InputStream tmpIn = null;
                OutputStream tmpOut = null;
                Message msg = new Message();
                try {
                    tmpIn = socket.getInputStream();
                    tmpOut = socket.getOutputStream();
                } catch (IOException e) {
                    msg.what =SOCKET_NOT_CREATED ;
                    mHandler.sendMessage(msg);
                    return;
                }
                mmInStream = tmpIn;
                mmOutStream = tmpOut;
                msg.what =STATE_CONNECTED ;
                mHandler.sendMessage(msg);

            }
            public void write(byte[] buffer) {
                try {
                    mmOutStream.write(buffer);

                    // Share the sent message back to the UI Activity
                } catch (IOException e) {
                    Message msg = new Message();
                    msg.what =WRITE_IO_ERROR ;
                    mHandler.sendMessage(msg);
                }
            }
            public void cancel() {
                try {
                    mmSocket.close();
                } catch(IOException e) {
                    return;
                }
                return;
            }

        }

        public void disconnect(){
            Message msg = new Message();
            if (connectTd != null){
                connectTd.cancel();
                connectTd = null;
            }

            if(connectedTd != null){
                connectedTd.cancel();
                connectedTd = null;
            }
            msg.what =STATE_NONE ;
            mHandler.sendMessage(msg);
        }
    }

    private Handler mHandler = new Handler() {
        @Override
        public void handleMessage (Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case CONNECT_DEVICE_FAIL:
                    Toast.makeText(MainActivity.this,
                            "Device connect fail", Toast.LENGTH_SHORT).show();
                    stateTextView.setText("disconnect");
                    break;
                case CONNECT_FAIL:
                    Toast.makeText(MainActivity.this,
                            " socket connect fail", Toast.LENGTH_SHORT).show();
                    stateTextView.setText("disconnect");
                    break;
                case SOCKET_NOT_CREATED:
                    Toast.makeText(MainActivity.this,
                            " socket not  create", Toast.LENGTH_SHORT).show();
                    stateTextView.setText("disconnect");
                    break;
                case WRITE_IO_ERROR:
                    Toast.makeText(MainActivity.this,
                            " can not send msg", Toast.LENGTH_SHORT).show();
                    //stateTextView.setText("not connect");
                    break;
                case STATE_CONNECTED:
                    Toast.makeText(MainActivity.this,
                            " connected", Toast.LENGTH_SHORT).show();
                    stateTextView.setText("connected");
                    break;
                case STATE_NONE:
                    Toast.makeText(MainActivity.this,
                            " disconnected", Toast.LENGTH_SHORT).show();
                    stateTextView.setText("disconnected");
                default:
                    return;
                }
            }
        };

}
