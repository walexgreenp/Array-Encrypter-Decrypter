.data

krabby: .word 1 2 3 4 5 6 7 8 9 10

carray: .word 0:10

marray: .word 0:10

.text
main:
	li $t0 3	# $t0 is a (3)
	li $t1 11	# $t1 is b (11)

	la $a0,krabby
	li $a1,10

	la $a2,carray
	la $a3,marray
	
	# fill in your loop here
	# feel free to use 2 loops if you need to
	
	# Working on just 1 value in array
	move $s0 $t0
	move $s1 $t1
	lw $s2 12($a0)
	
	addiu $sp $sp -8
	sw $t0 0($sp)
	sw $t1 4($sp)

	jal secret_formula_apply

	lw $t0 0($sp)
	lw $t1 4($sp)
	addiu $sp $sp 8

	move $a0 $v0
	li $v0 1
	syscall
	

	j exit





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
	li $t0 7	# $t0 is e
	mult $s0 $s1
	mflo $t1	# $t1 is n

	# Power function
	move $t2 $s2	# $t2 same val as $s2, c
	li $t3 1	# i = 1

loop_body:

    beq $t3 $t0 loop_exit
    mult $t2 $t2
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
# ---------------------------------------------------------------





secret_formula_remove:
#fill more stuff here thanks

exit:
	li $v0, 10
	syscall


