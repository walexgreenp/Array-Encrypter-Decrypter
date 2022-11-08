.data

	krabby: .word 1 2 3 4 5 6 7 8 9 10
	carray: .word 0:10
	marray: .word 0:10

	encrypted_text: .asciiz "Encrypted: "
	decrypted_text: .asciiz "\nDecrypted: "
	new_space: .asciiz ", "




.text
# MAIN --------------------------------------------------------
main:
	# Setting values of a and b
	li $t0 3	# $t0 is a (3)
	li $t1 11	# $t1 is b (11)

	# Setting arrays to $a* registers (from template)
	la $a0 krabby
	li $a1 10
	la $a2 carray
	la $a3 marray



	# ENCRYPT ------------------------------------

	# Loop setup
	move $t3 $a1	# 10
	li $t4 0		# i

apply_encrypt_loop:
	# Placing parameters into s registers
	move $s0 $t0
	move $s1 $t1
	lw $s2 0($a0)

	# Putting onto stack
	beq $t3 $t4 after_encrypt_loop
	addiu $sp $sp -16
	sw $t0 0($sp)
	sw $t1 4($sp)
	sw $t3 8($sp)
	sw $t4 12($sp)

	# Function call
	jal secret_formula_apply

	# Retrieving from stack
	lw $t0 0($sp)
	lw $t1 4($sp)
	lw $t3 8($sp)
	lw $t4 12($sp)
	addiu $sp $sp 16

	move $t2 $v0 # Value after encryption

	# Storing value into array, adding 4 to go to next array index
	sw $t2 0($a2)
	addi $a0 $a0 4
	addi $a2 $a2 4
	# Add 1 to i, jump back to loop
	addi $t4 $t4 1

	j apply_encrypt_loop


after_encrypt_loop:
	addi $a2 $a2 -40 # Moves array pointer to start like normal

	# PRINT AREA
	# Print "Encrypted: " text
	li $v0 4
	addiu $sp $sp 4
	sw $a0 0($sp)
    la $a0 encrypted_text
	syscall
	lw $a0 0($sp)
	addiu $sp $sp -4

	# Loop setup
	li $t3 10
	li $t4 0


carray_print_loop:
	# Print value(s)
	beq $t3 $t4 carray_loop_end

	lw $t5 0($a2)
	li $v0 1
	move $a0 $t5
	syscall

	addi $t6 $t4 1
	beq $t6 $t3 carray_loop_end

	li $v0 4
	la $a0 new_space
	syscall

	addiu $a2 $a2 4
	addiu $t4 $t4 1

	j carray_print_loop


carray_loop_end:

	li $v0 4
	addiu $sp $sp 4
	sw $a0 0($sp)
    la $a0 decrypted_text
	syscall
	lw $a0 0($sp)
	addiu $sp $sp -4

	# CLEAN SLATE DECRYPT -------------------------

	move $t3 $a1	# 10
	li $t4 0

	addi $a2 $a2 -36
	
	# Putting arguments into "$s*" registers
	move $s0 $t0
	move $s1 $t1
	la $s2 0($a2)

	addiu $sp $sp -24
	lw $t0 0($sp)
	lw $t1 4($sp)
	lw $t2 8($sp)
	lw $t3 12($sp)
	lw $t4 16($sp)
	lw $t5 20 ($sp)

	jal secret_formula_remove

	sw $t0 0($sp)
	sw $t1 4($sp)
	sw $t2 8($sp)
	sw $t3 12($sp)
	sw $t4 16($sp)
	sw $t5 20 ($sp)
	addiu $sp $sp 24



# loop through 10 times, add 4 each time, print

	addiu $a2 -40

	# Loop setup
	li $t3 10
	li $t4 0
marray_print_loop:
	# Print value(s)
	beq $t3 $t4 marray_loop_end

	lw $t5 0($a2)
	li $v0 1
	move $a0 $t5
	syscall

	addi $t6 $t4 1
	beq $t6 $t3 marray_loop_end

	li $v0 4
	la $a0 new_space
	syscall

	addiu $a2 $a2 4
	addiu $t4 $t4 1

	j marray_print_loop

marray_loop_end:






	j exit
# MAIN --------------------------------------------------------











# SECRET_FORMULA_APPLY ----------------------------------------
secret_formula_apply:
	# Variables used: s0, s1, s2, ra
	# Storing variables on the stack
	addiu $sp $sp -16
	sw $s0 0($sp)	# $s0 is x
	sw $s1 4($sp)	# $s1 is y
	sw $s2 8($sp)	# $s2 is m
	sw $ra 12($sp)

	# Program
	li $t0 7	# $t0 is WHAT IS PUT INTO e (7)
	mult $s0 $s1
	mflo $t1	# $t1 is n

	# Power function
	move $t2 $s2	# $t2 same val as $s2, c
	li $t3 1	# i = 1
	move $t4 $t2

loop_body:

    beq $t3 $t0 loop_exit
    mult $t2 $t4
    mflo $t2
    addi $t3 $t3 1

    j loop_body

loop_exit:
	# Getting mod after power function
	div $t2 $t1
	mfhi $v0

	# Getting data back from the stack
	lw $s0 0($sp)
	lw $s1 4($sp)
	lw $s2 8($sp)
	lw $ra 12($sp)
	addiu $sp $sp 16

	jr $ra
# SECRET_FORMULA_APPLY ----------------------------------------










# SECRET_FORMULA_REMOVE ---------------------------------------
secret_formula_remove:
	addiu $sp $sp -16
	sw $s0 0($sp)	# ($s0) is x
	sw $s1 4($sp)	# ($s1) is y
	sw $s2 8($sp)	# ($s2) is c
	sw $ra 12($sp)	

	li $t0 3	# 3 is d ($t0)
	mult $s0 $s1
	mflo $t1 	# $t1 (n)

	move $t2 $s2	# $t2 is c

	li $t3 0	# i is $t3 (0)
	move $t4 $t2

while_remove:
	beq $t3 $t0 while_exit
	mult $t2 $t4
	mflo $t2
	addi $t3 $t3 1

	j while_remove

while_exit:
	div $t2 $t1
	mfhi $v0
 
	lw $s0 0($sp)
	lw $s1 4($sp)
	lw $s2 8($sp)
	lw $ra 12($sp)
	addiu $sp $sp 16

	jr $ra





# SECRET_FORMULA_REMOVE ---------------------------------------


exit:
	li $v0, 10
	syscall


