# VinUni Hacking Club Boot2Root Challenge - CECS Day 2024!!!

## Description 📝

Just a simple boot2root challenge from the VinUni Hacking Club. Goal is gaining RCE -> root. 
Also some simple koth challenges. :)))

## Rulessss 📑

### Targets 🎯

There will be a vulnerable machine running on a specific address that we will provide. Your targets:
- [ ] Being the root (simple words: `id -> uid=0(root) gid=0(root) groups=0(root)`)
- [ ] Writing your name in the file `/root/king.txt` (you can use `echo "your_name" > /root/king.txt`). We will count your score based on this file.
  - In case someone replaced you as the king, and you regain the control, we recommend you should not change your name into a new one. (e.g. `ice` or `1c3` will be counted as 2 different names) 
  - The first time you become the root, you will gain 500 points. For each 10 minutes you are the king, additional 100 points. 
  - Retaking the king position will gain you as the first time. (e.g. if A is the king, B takes over (right after A), then A retakes the king position, A will gain 1000 points)
- [ ] Patch the vulns (to root, or to RCE, based on your needs) (you have only 5 minutes to do this, we will shut all the process that is not ours down)
  - If you need to run a service inside, name it `patch`, else we will shut it down `:)`

### Final Score 🏆

The only winner is the one who has the highest score. The score will be updating every 10 minutes. 

## Files 📁

```
./monitor: A simple script to monitor the king position
./sources: Source code of the challenges
./README.md: This file
Dockerfile: Dockerfile to build the image
```