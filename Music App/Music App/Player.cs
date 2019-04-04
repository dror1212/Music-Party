using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Android.App;
using Android.Content;
using Android.Media;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;

namespace Music_App
{
    [Service]
    
    [IntentFilter(new[] { ActionPlay, ActionPause, ActionStop })]
    class Player : Service
    {
        public const string ActionPlay = "com.xamarin.action.PLAY";
        public const string ActionPause = "com.xamarin.action.PAUSE";
        public const string ActionStop = "com.xamarin.action.STOP";
        private MediaPlayer player;
        public override IBinder OnBind(Intent intent)
        {
            throw new NotImplementedException();
        }

        public override void OnCreate()
        {
            base.OnCreate();
        }
        public override void OnDestroy()
        {
            base.OnDestroy();
        }
        [return: GeneratedEnum]
        public override StartCommandResult OnStartCommand(Intent intent, [GeneratedEnum] StartCommandFlags flags, int startId)
        {
            Play();
            //Set sticky as we are a long running operation
            return StartCommandResult.Sticky;
        }
        private async System.Threading.Tasks.Task Play()
        {
            player = new MediaPlayer();
            //Tell our player to stream music
            player.SetAudioStreamType(Stream.Music);
            //When we have prepared the song start playback
            player.Prepared += (sender, args) => player.Start();
            //When we have reached the end of the song stop ourselves, however you could signal next track here.
            player.Completion += (sender, args) => Stop();
            player.Error += (sender, args) =>
            {
                //playback error
                Console.WriteLine("Error in playback resetting: " + args.What);
                Stop();//this will clean up and reset properly.

            };
            await player.SetDataSourceAsync(ApplicationContext, Android.Net.Uri.Parse("https://www.youtube.com/watch?v=zaf6StO4gy4"));
            player.PrepareAsync();
        }
        private void Stop()
        {

        }
        private void Pause()
        {

        }

    }
}