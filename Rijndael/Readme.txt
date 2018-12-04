                        ------------------------------
                        Rijndael ANSI C Reference Code
                        ------------------------------

                                October 24, 2000

                                  Disclaimer


This software package was submitted to the National Institute of Standards and
Technology (NIST) during the Advanced Encryption Standard (AES) development
effort by Joan Daemen and Vincent Rijmen, the developers of the Rijndael algorithm.

This software is distributed in compliance with export regulations (see below), and
it is intended for non-commercial use, only.   NIST does not support this software 
and does not provide any guarantees or warranties as to its performance, fitness 
for any particular application, or validation under the Cryptographic Module
Validation Program (CMVP) <http://csrc.nist.gov/cryptval/>.  NIST does not accept 
any liability associated with its use or misuse.  This software is provided as-is. 
By accepting this software the user agrees to the terms stated herein.

                            -----------------------

                              Export Restrictions


Implementations of cryptography are subject to United States Federal
Government export controls.  Export controls on commercial encryption products 
are administered by the Bureau of Export Administration (BXA) 
<http://www.bxa.doc.gov/Encryption/> in the U.S. Department of Commerce. 
Regulations governing exports of encryption are found in the Export 
Administration Regulations (EAR), 15 C.F.R. Parts 730-774.

=====================================================================================

Rijndael
Joan Daemen

Reference Implementation (+ KATs and MCTs)  v2.0
-----------------------------------------------------------

This archive contains the following files:

Makefile.bcc:	    makefile for use with Borland compiler.
Makefile.gcc:	    makefile for use with GCC-based compilers.
Makefile.Visualc:   makefile for use with Visual C compiler.
README: 	    This file.
boxes-ref.dat:	    Tables that are needed by the reference implementation.
		    The tables implement the S-box and its inverse, and also
		    some temporary tables needed for multiplying in the finite
		    field GF(2^8).
rijndael-alg-ref.c:
rijndael-alg-ref.h:
		    Algorithm implementation.
rijndael-api-ref.c:
rijndael-api-ref.h:
		    Interface to the C API.
rijndaeltest-ref.c:
		    Implementation of the KAT and MCT.
table.128:
table.192:
table.256:
		Files needed for the KAT (for the Table Known Answer Test).



Instructions for the KAT and MCT software:

1) Compile the C code and put the executable in the same directory as the
   table.??? files.
2) Run the executable. It generates all the tables in the NIST format.
3) Compare the generated tables with the original provided tables, e.g.
   in Unix, with `diff'. 
   
   
Changes with respect to v1.0 (= round 1 submission)
---------------------------------------------------

1) Removed the parameter blockLen from makeKey() and cipherInit().
   The parameter is still present in the structures keyInstance and
   cipherInstance.
   
   
