# cs64_lab05a
Collaborated with Jacey Buchner, jbuchner@ucsb.edu


In the README.txt please explain what you think the “secret formula” file is doing (in one paragraph, 3+ lines). (5 points)

I believe what will happen is that there will be an array passed into krabby, which throughout the code we will have to edit. After taking in that array, all of the values will be parsed through and edited based on the formula that is in the secret_formula_apply function. The secret_formula_apply function basically takes the value, takes it to the power of a constant, and then outputs the remainder of that value divided with another constant. The program stores this into c_arr, and then does something similar but instead decodes it this time in the secret_formula_remove. This gets stored into m_arr, and prints out both c_arr and m_arr, m_arr which should be the original array.


(i) c[i]=secret_formula_apply(u[i]), f[i]=secret_formula_apply(t[i]), then does u[i]*t[i] = secret_formula_remove(c[i]*f[i]) hold for all entries in both arrays? (2.5 points)

This does hold for both entries in the array. The outputs will be the same as what would happen in secret_formula_asm. 


(ii) c[i]=secret_formula_apply(u[i]), f[i]=secret_formula_apply(t[i]), then does u[i]+t[i] = secret_formula_remove(c[i]+f[i]) hold for all entries in both arrays? (2.5 points)

This does not hold for both entries in the array, since the outputs are different. u = 0x03; t = 0x07, doesnt work. 