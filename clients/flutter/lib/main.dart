import 'package:flutter/material.dart';
void main()=>runApp(const AudioHardcoreApp());
class AudioHardcoreApp extends StatelessWidget{const AudioHardcoreApp({super.key});@override Widget build(BuildContext context)=>MaterialApp(title:'AudioHardcore',theme:ThemeData(useMaterial3:true),home:const LibraryShell());}
class LibraryShell extends StatelessWidget{const LibraryShell({super.key});@override Widget build(BuildContext context)=>Scaffold(appBar:AppBar(title:const Text('AudioHardcore')),body:const Center(child:Text('Shared client scaffold — connect to the AudioHardcore API.')));}
