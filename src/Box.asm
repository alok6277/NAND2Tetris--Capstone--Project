
// ==========================================
// NAND2TETRIS CAPSTONE PROJECT
// BIG CENTERED FILLED BLACK BOX
// ==========================================

// Screen size: 512 x 256 pixels
// Box width: 128 pixels
// Box height: 80 rows
// Starting X: 192
// Starting Y: 88

// Starting address = 16384 + (88 * 32) + 12

@19212
D=A
@R0
M=D

// Number of rows = 80

@80
D=A
@R1
M=D

(ROW)

// Number of 16-bit words per row = 8

@8
D=A
@R2
M=D

(COL)

// Draw 16 black pixels

@R0
A=M
M=-1

// Move to next 16-bit word

@R0
M=M+1

// Decrease column counter

@R2
MD=M-1

@COL
D;JGT

// Move to next screen row
// Skip remaining 24 words

@24
D=A
@R0
M=D+M

// Decrease row counter

@R1
MD=M-1

@ROW
D;JGT

// Infinite loop

(END)
@END
0;JMP
