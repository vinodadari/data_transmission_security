# Device Transmission Security

## Encryption Technologies
* Transport Layer Security (TLS)
* End-to-End Encryption (E2EE)

## Transport Layer Security (TLS):

### What it is:

 TLS is a cryptographic protocol that encrypts data in transit between two applications communicating over a network. It's the industry standard for securing communication on the internet.

Always Encrypted: Data in transit (between devices and servers) is encrypted using TLS.

### How it works:

When you connect to a website or use a secure app, TLS establishes a secure connection between your device and the server. This involves:

Handshake:

Client and server negotiate encryption algorithms and exchange certificates to verify each other's identity.

Encryption:

Data exchanged between the client and server is encrypted using the agreed-upon algorithms. This makes it unreadable to anyone intercepting the data stream.

### Benefits:

Protects data confidentiality: Encrypted data cannot be understood by unauthorized users.

Ensures data integrity: TLS helps detect any tampering with the data during transmission.

Provides authentication: It helps verify the identity of the server you're communicating with (important for preventing man-in-the-middle attacks).

### Limitations:

Doesn't encrypt data at rest: Once data reaches the server and is stored, TLS doesn't protect it.

Relies on server certificates: If a certificate is compromised, the security of the connection can be breached.


## End-to-End Encryption (E2EE):

### What it is:

E2EE is a security concept where data is encrypted not only in transit but also at rest on servers. This means only the authorized participants (sender and recipient) can decrypt the communication.

### How it works:

With E2EE, the message content is encrypted using keys that are unique to the communicating devices. These keys are never shared with the server, so even the server that facilitates the communication cannot decrypt the message content.

### Benefits:

Provides the strongest level of data confidentiality: Only authorized users can access the message content.

### Limitations:

Requires complex key management: Distributing and managing encryption keys securely can be challenging.

May not be supported by all communication platforms.

Forwarding messages or recovering lost messages can be difficult without additional mechanisms.
