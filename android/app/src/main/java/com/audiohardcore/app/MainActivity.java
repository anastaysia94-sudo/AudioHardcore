package com.audiohardcore.app;

import android.Manifest;
import android.app.Activity;
import android.content.ContentUris;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {
    private final List<String> allTitles = new ArrayList<>();
    private final List<Uri> allUris = new ArrayList<>();
    private final List<String> titles = new ArrayList<>();
    private final List<Uri> uris = new ArrayList<>();
    private ArrayAdapter<String> adapter;
    private TextView status, nowPlaying;
    private static final int REQ = 44;

    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        setContentView(com.audiohardcore.app.R.layout.activity_main);
        status = findViewById(R.id.status); nowPlaying = findViewById(R.id.nowPlaying);
        ListView list = findViewById(R.id.trackList); EditText search = findViewById(R.id.searchBox);
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, titles);
        list.setAdapter(adapter);
        list.setOnItemClickListener((p,v,pos,id) -> play(uris.get(pos), titles.get(pos)));
        search.addTextChangedListener(new TextWatcher(){ public void beforeTextChanged(CharSequence s,int a,int c,int d){} public void onTextChanged(CharSequence s,int a,int b,int c){ filter(s.toString()); } public void afterTextChanged(Editable e){} });
        requestAndLoad();
    }
    private void requestAndLoad(){
        String permission = android.os.Build.VERSION.SDK_INT >= 33 ? Manifest.permission.READ_MEDIA_AUDIO : Manifest.permission.READ_EXTERNAL_STORAGE;
        if (checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED) requestPermissions(new String[]{permission}, REQ); else loadMusic();
    }
    @Override public void onRequestPermissionsResult(int r,String[] p,int[] g){ super.onRequestPermissionsResult(r,p,g); if(r==REQ && g.length>0 && g[0]==PackageManager.PERMISSION_GRANTED) loadMusic(); else status.setText("Audio permission is required to scan your local library."); }
    private void loadMusic(){
        status.setText("Scanning local music…");
        allTitles.clear(); allUris.clear(); titles.clear(); uris.clear();
        String[] proj={MediaStore.Audio.Media._ID,MediaStore.Audio.Media.TITLE,MediaStore.Audio.Media.ARTIST,MediaStore.Audio.Media.IS_MUSIC};
        String sel=MediaStore.Audio.Media.IS_MUSIC+"!=0";
        try(Cursor c=getContentResolver().query(MediaStore.Audio.Media.EXTERNAL_CONTENT_URI,proj,sel,null,MediaStore.Audio.Media.TITLE+" COLLATE NOCASE")){
            if(c!=null) while(c.moveToNext()){
                long id=c.getLong(0); String title=c.getString(1); String artist=c.getString(2);
                allTitles.add((artist==null?"Unknown Artist":artist)+" — "+(title==null?"Unknown Track":title));
                allUris.add(ContentUris.withAppendedId(MediaStore.Audio.Media.EXTERNAL_CONTENT_URI,id));
            }
        }
        titles.addAll(allTitles); uris.addAll(allUris); adapter.notifyDataSetChanged(); status.setText(titles.size()+" tracks available on this device");
    }
    private void filter(String q){
        if(q==null) q=""; q=q.toLowerCase();
        titles.clear(); uris.clear();
        for(int i=0;i<allTitles.size();i++) if(allTitles.get(i).toLowerCase().contains(q)){ titles.add(allTitles.get(i)); uris.add(allUris.get(i)); }
        adapter.notifyDataSetChanged();
    }
    private void play(Uri uri,String label){
        try{
            Intent intent=new Intent(this, PlaybackService.class);
            intent.putExtra("uri",uri); intent.putExtra("title",label);
            if(android.os.Build.VERSION.SDK_INT>=26) startForegroundService(intent); else startService(intent);
            nowPlaying.setText("▶ "+label);
        } catch(Exception e){ nowPlaying.setText("Unable to play: "+label); }
    }
}
