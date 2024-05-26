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
  - Retaking the king position will gain you as the first time, PLUS 25% points of the previous king. 
    - Example: If A is the king, then after 10 minutes, B becomes the king, then again after 10 minutes, A becomes the king:
      - B will gain: 500 + 500*0.25 = 625 points
      - A will gain: 500 + 500 + 625*0.25 = 1250 points
  - The king will be updated every 10 minutes.
- [ ] Patch the vulns (to root, or to RCE, based on your needs) (you have only 10 minutes to do this CONTINUOUSLY, we will shut all the process that is not ours down)
  - If you need to run a service inside, name it `patch_{yournamehere}`, else we will shut it down `:)`

### Final Score 🏆

The only winner is the one who has the highest score. The score will be updating every 10 minutes. 

### Toolings ☢

The usage of tools is allowed, but we recommend you not to install any new softwares to the system (in case you got RCE). We provided these default tools: 

+ `bash`
+ `python3` with support of 2 libraries: `pycryptodome` and `pwntools`
+ `nvim`
+ `gdb` with support of `gef`

Indeed, with your programming & Linux skills, we are sure that you will survive :)

### Ban 🚫

- No DDoS/brute-forcing that makes the server corrupt :( No one asked you to spoil the fun. 
- No sharing vulns, but discussing is allowed (and heavily recommended!).
- There are some commands that you MUST NOT run: 
  - `rm` 
  - `chpasswd`/`passwd`/... that changes the password of the root user
  - ... Anything that makes the server unstable/spoil the fun :( 

## Files 📁

```
./monitor: A simple script to monitor the king position
./sources: Source code of the challenges
./README.md: This file
```

Each folder will have its own README to let you know what to do.