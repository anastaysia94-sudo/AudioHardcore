package com.audiohardcore.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;

public class PlaybackService extends Service {
    private static final String CHANNEL = "audiohardcore-playback";
    private MediaPlayer player;

    @Override public void onCreate() {
        super.onCreate();
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel channel = new NotificationChannel(CHANNEL, "AudioHardcore playback", NotificationManager.IMPORTANCE_LOW);
            getSystemService(NotificationManager.class).createNotificationChannel(channel);
        }
    }

    @Override public int onStartCommand(Intent intent, int flags, int startId) {
        Uri uri = intent == null ? null : intent.getParcelableExtra("uri");
        String title = intent == null ? "AudioHardcore" : intent.getStringExtra("title");
        if (uri != null) play(uri, title == null ? "AudioHardcore" : title);
        return START_NOT_STICKY;
    }

    private void play(Uri uri, String title) {
        release();
        try {
            player = new MediaPlayer();
            player.setAudioAttributes(new AudioAttributes.Builder().setContentType(AudioAttributes.CONTENT_TYPE_MUSIC).setUsage(AudioAttributes.USAGE_MEDIA).build());
            player.setDataSource(this, uri);
            player.setOnCompletionListener(p -> stopSelf());
            player.prepare();
            player.start();
            Notification.Builder builder = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, CHANNEL) : new Notification.Builder(this);
            builder.setContentTitle("AudioHardcore").setContentText(title).setSmallIcon(android.R.drawable.ic_media_play).setOngoing(true);
            startForeground(1001, builder.build());
        } catch (Exception ex) {
            stopForeground(true);
            stopSelf();
        }
    }

    private void release() { if (player != null) { try { player.stop(); } catch (Exception ignored) {} player.release(); player = null; } }
    @Override public void onDestroy() { release(); super.onDestroy(); }
    @Override public IBinder onBind(Intent intent) { return null; }
}
