# How to Solve the RC4 puzzle

## Background

RC4 is similar to a one-time-pad XOR cipher. But to save having to exchange long, single use secrets, we share a short secret (_the key_), and use that to generate a longer secret (_the keystream_).

But we must not  reuse the shared secret - at least, not the same part of the longer secret.

## The Vulnerable System

We have a server that exchanges RC4 encrypted messages. But we see that when we send the same message again, the encryped value is identical. So we know that it's reusing the key.

How can we use this knowledge to break the system?

It's important that we do not need _the key_ to decrpyt the secret. Only _the keystream_.
To encrypt, the server runs:

    ciphertext = secret XOR keystream

To get the keystream, we can run

    keystream = secret XOR ciphertext

All we need is a known pair of ciphertext & secret (plaintext). We can get that by getting the server to encrypt a plaintext. Make sure it's longer than the secret you want to decrypt - otherwise you won't have enough keystream.

## Step by step

1. Send a plaintext for encryption. Put "AAAAAAAAAAAAAAAAAAAAAAAAA" in the secret box. Click _submit_.
2. Get the keystream by XOR'ing the ciphertext against your plaintext (don't forget that the ciphertext is base64 encoded)

JavaScript Example

    var c = atob(CIPHERTEXT); // base64 decode
    var p = "AAAAAAAAAAAAAAAAAAAAAAAAA"; // known plaintext
    var keystream = [];
    for (var i = 0; i < c.length; i++){
        keystream.push( c.charCodeAt(i) ^ p.charCodeAt(i)); // "^" is XOR
    }

3. Get the secret plaintext by XOR'ing the secret ciphertext against the keystream

JavaScript Example

    var secret = atob("0J3/koz8ZH+sOoulenw0iA=="); // base64 decode
    var result = [];
    for (var i = 0; i < secret.length; i++){
        result.push( secret.charCodeAt(i) ^ keystream[i]);
    }
    String.fromCharCode(...result); // Convert bytes to chars