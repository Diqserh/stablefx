const express=require('express');
const path=require('path');
const app=express();
const PORT=process.env.PORT||3000;
app.use(express.static(__dirname));
app.get('/api/rates',(req,res)=>res.json({
  'USDC/EURC':0.9245,'EURC/USDC':1.0817,
  'USDC/GBPC':0.7923,'GBPC/USDC':1.2622,
  'USDC/USDT':1.0001,'USDT/USDC':0.9999,
  'EURC/GBPC':0.8571,'GBPC/EURC':1.1667
}));
app.get('/api/health',(req,res)=>res.json({status:'ok',time:new Date()}));
app.get('*',(req,res)=>res.sendFile(path.join(__dirname,'index.html')));
app.listen(PORT,()=>console.log('StableFX on port '+PORT));
