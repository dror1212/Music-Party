using Android.App;
using Android.Widget;
using Android.OS;
using Android.Support.V7.App;
using System.Net.Sockets;
using System.Threading;
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
        private byte[] datalength;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);
            btnSend = FindViewById<Button>(Resource.Id.btnSend);
            edt1 = FindViewById<EditText>(Resource.Id.edt1);
            btnSend.Click += BtnSend_Click;
            datalength = new byte[32];
        }

        private void BtnSend_Click(object sender, System.EventArgs e)
        {
            client = new TcpClient("10.30.56.204", 3334);
            clientReceive();
        }

        private void clientReceive()
        {
            try
            {
                stream = client.GetStream(); //Gets The Stream of The Connection
                new Thread(() => // Thread (like Timer)
                {
                    while (true)//Keeps Trying to Receive the Size of the Message or Data
                    {
                        if ((stream.Read(datalength, 0, 32)) != 0)
                        {
                            this.RunOnUiThread(() => this.edt1.Text = this.edt1.Text + "kkk");
                        }
                    }
                }).Start(); // Start the Thread
            }
            catch (Exception ex)
            {
                Toast.MakeText(this, ex.Message, ToastLength.Short).Show();
            }
        }
    }
}

