using Android.App;
using Android.Widget;
using Android.OS;
using Android.Support.V7.App;
using System.Net.Sockets;
using System.Threading;
using Android.Media;
using System;
using System.Text;

namespace music
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        Button btnSend;
        EditText edt1;
        TcpClient client;
        NetworkStream stream;
        AudioTrack player;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);
            btnSend = FindViewById<Button>(Resource.Id.btnSend);
            edt1 = FindViewById<EditText>(Resource.Id.edt1);
            player = new AudioTrack(global::Android.Media.Stream.Music, 88000, ChannelOut.Mono, Android.Media.Encoding.Pcm16bit,32,AudioTrackMode.Stream);
            btnSend.Click += BtnSend_Click;
        }

        private void BtnSend_Click(object sender, System.EventArgs e)
        {
            client = new TcpClient("192.168.1.105", 3334);
            clientReceive();
        }

        private void clientReceive()
        {
            try
            {
                stream = client.GetStream(); //Gets The Stream of The Connection
                //byte[] x = System.Text.Encoding.ASCII.GetBytes("Connection:d,1");
                //stream.Write(x, 0, x.Length);
                player.Play();
                new Thread(() => // Thread (like Timer)
                {
                    while (true)//Keeps Trying to Receive the Size of the Message or Data
                    {
                        byte[] datalength = new byte[32];
                        if ((stream.Read(datalength, 0, 32)) != 0)
                        {
                            this.RunOnUiThread(() => PlaySound(datalength));
                        }
                    }
                }).Start(); // Start the Thread
            }
            catch (Exception ex)
            {
                Toast.MakeText(this, ex.Message, ToastLength.Short).Show();
            }
        }

        private void PlaySound(byte[] data)
        {
            player.Write(data, 0, 32);
        }
    }
}

