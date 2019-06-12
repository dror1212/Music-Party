using Android.App;
using Android.Widget;
using Android.OS;
using Android.Support.V7.App;
using System.Net.Sockets;
using System.Threading;
using Android.Media;
using System;
using System.Text;
using Java.Lang;
using System.IO;

namespace music
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        Button btnSend,btnSend1;
        EditText edt1;
        TcpClient client;
        NetworkStream stream;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);
            btnSend = FindViewById<Button>(Resource.Id.btnSend);
            btnSend1 = FindViewById<Button>(Resource.Id.btnSend1);
            edt1 = FindViewById<EditText>(Resource.Id.edt1);
            btnSend.Click += BtnSend_Click;
        }

        private void BtnSend_Click(object sender, System.EventArgs e)
        {
            client = new TcpClient("10.30.57.160", 3540);
            clientReceive();
        }

        private void clientReceive()
        {
            try
            {
                stream = client.GetStream(); //Gets The Stream of The Connection
                //byte[] x = System.Text.Encoding.ASCII.GetBytes("Connection:d,1");
                //stream.Write(x, 0, x.Length);
                //new System.Threading.Thread(() => // Thread (like Timer)
                //{
                while (true)//Keeps Trying to Receive the Size of the Message or Data
                {
                    byte[] datalength = new byte[32468];
                    if ((stream.Read(datalength, 0, 32468)) != 0)
                    {
                        PlaySound(datalength);
                    }
                }
                //}).Start(); // Start the Thread
            }
            catch (System.Exception ex)
            {
                Toast.MakeText(this, ex.Message, ToastLength.Short).Show();
            }
        }

        private void PlaySound(byte[] data)
        {
            try
            {
                AudioTrack player = new AudioTrack(Android.Media.Stream.Music, 88000, ChannelOut.Default, Android.Media.Encoding.Pcm16bit, 32468, AudioTrackMode.Static);
                player.Write(data, 0, 32468);
                //Toast.MakeText(this, "start playing", ToastLength.Short).Show();
                //if (player.PlayState!=PlayState.Playing)
                player.Play();
            }
            catch(IllegalStateException ex)
            {
                Toast.MakeText(this, ex.Message, ToastLength.Short).Show();
            }
        }
    }
}

