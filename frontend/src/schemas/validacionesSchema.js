import * as yup from 'yup';


export const loginSchema = yup.object({

    correo: yup.string().required("El campo correo es obligatorio").email("El correo ingresado no es valido"),
    password:  yup.string().required("El campo password es obligatorio")
});
