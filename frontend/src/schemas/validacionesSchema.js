import * as yup from 'yup';


export const loginSchema = yup.object({

    correo: yup.string().required("El campo correo es obligatorio").email("El correo ingresado no es valido"),
    password:  yup.string().required("El campo password es obligatorio")
});


export const librosSchema = yup.object({

    categoria_id: yup.string().test({
        name: 'categoria_id',
        skipAbsent: true,
        test(value, ctx){
            if(value == 0){
                return ctx.createError({
                    message: "Debe de seleccionar una categoria."
                })
            }
            return true;
        }
    }),
    nombre:  yup.string().required("El campo nombre es obligatorio"),
    autor:  yup.string().required("El campo autor es obligatorio"),
    descripcion:  yup.string().required("El campo descripcion es obligatorio"),
});

