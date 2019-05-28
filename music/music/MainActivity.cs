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
            btnSend1.Click += BtnSend1_Click;
        }

        private void BtnSend1_Click(object sender, EventArgs e)
        {
            var bytes = default(byte[]);
            using (var streamReader = new StreamReader("C:\\Users\\student\\Desktop\\Music-Party-check\\songs\\Counting Stars.wav"))
            {               
                using (var memstream = new MemoryStream())
                {
                    streamReader.BaseStream.CopyTo(memstream);
                    bytes = memstream.ToArray();
                }
            }
            int max = 33;
            int count = 0;
            while(true)
            {
                byte[] b = new byte[32];
                int count2 = count;
                while (count2 < max)
                {
                    b[count] = bytes[count];
                    count2 = count2+1;
                }
                count = max;
                max = max + max - 1;
                PlaySound(bytes);
            };
        }

        private void BtnSend_Click(object sender, System.EventArgs e)
        {
            client = new TcpClient("10.30.57.145", 3539);
            clientReceive();
        }

        private void clientReceive()
        {
            try
            {
                stream = client.GetStream(); //Gets The Stream of The Connection
                //byte[] x = System.Text.Encoding.ASCII.GetBytes("Connection:d,1");
                //stream.Write(x, 0, x.Length);
                new System.Threading.Thread(() => // Thread (like Timer)
                {
                    while (true)//Keeps Trying to Receive the Size of the Message or Data
                    {
                        byte[] datalength = new byte[32];
                        if ((stream.Read(datalength, 0, 32)) != 0)
                        {
                            PlaySound(datalength);
                        }
                    }
                }).Start(); // Start the Thread
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
#pragma warning disable CS0618 // Type or member is obsolete
                AudioTrack player = new AudioTrack(Android.Media.Stream.Music, 8000, ChannelOut.Mono, Android.Media.Encoding.Pcm16bit, 32, AudioTrackMode.Static);
#pragma warning restore CS0618 // Type or member is obsolete
                player.Write(data, 0, 32);
                player.Play();
            }
            catch(IllegalStateException)
            {}
        }
    }
}

