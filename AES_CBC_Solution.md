# How to Solve the AES CBC puzzle

## Background

AES is an encryption system that accepts a 16 byte key, and a 16 byte plaintext and outputs a 16 byte secret. For the purposes of this excercise, we will treat AES as an unbreakable black-box.

In AES _ECB mode_, each block of 16 bytes is encrypted separately, using the same key. One disadvantage with this is that identical plain blocks result in identical cipher blocks. As an improvement on this, we have Cipher Block Chaining (CBC) mode. Each block is XOR'ed with the ciphertext of the previous block before it is encrypted. The first block (has no previous block), is XOR'ed with a random Initialisation Vector (IV).

![AES CBC Mode](images/aes cbc mode.jpg?raw=true "AES CBC Mode")

_But what if the data doesn't fit neatly into a multiple of 16 bytes?_

To resolve this, we pad the data to become a multiple of 16 bytes, using a method called PKCS #7. If the data is one bytes short we put one extra byte, with the value

    0x01
    
If the data is 2 bytes short, we put 2 bytes

    0x02 0x02

All the way up 16 times 0x10 (decimal 16). To remove the padding, after decryption, the system checks the value of the last byte, and removes that many bytes from the end.


## The Vulnerable System

The server decrypts the messages, but does not show the result.
Its one weakness, is that if the padding does not match PKCS #7, we get an error _"invalid padding"_.

A small mistake, but enough to completely break the encryption.


## Step by step

We will start breaking the secret from the end, and work towards the start.

We know that we can affect the last byte of the ciphertext by changing the last byte of the previous block. Of course, this will completely garble the previous block, but at this stage we're only interested in the last block.

![CBC Break](images/cbc break step by step.jpg?raw=true "CBC Break - Step by Step")

We want to find _P_. And we know that

    (1)    P = X XOR I

We have _X_ from the real ciphertext. If we could know that a fake value of _X_ (_Xf_) would give us a known value of _P_ (_Pf_), then we could calculate the real value of _i_.


There are 256 possible bytes. If we try all the other 255 possibilities, only one of them will result in legal PKCS #7 padding. The one that results in 0x01 after decryption.

Then,

    (2)    i = Xf XOR Pf

Once we have _i_, we can calculate the real value of _P_ using formula (1).

To get the second last byte, we use the known value of _i_ to choose a value of _X_ that results in _P_ = 2. Then we brute force _Y_ 256 times, until _Q_ = 2. Now we can calulate _j_, and therefore the real value of _Q_.

We do this for the whole block.

To calculate the previous block, we can just remove the last 16 bytes, and work as if this is the last block.


At this point, we can find the real value of _i_ in the intermediate block, by XOR of the changed byte, with the known 