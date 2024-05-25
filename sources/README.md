Build command: 

```bash
docker build -t boot2root . 
docker run --name boot2root -v `pwd`/monitor/king.txt:/root/king.txt -d -p 80:5000 boot2root 
```