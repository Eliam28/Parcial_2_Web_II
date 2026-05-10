import DefaultLayout from "../layout/DefaultLayout"

function Register(){
    return <>
    <DefaultLayout>
        <form className="form">
            <h1>Registrar usuario</h1>

            <label>Nombre de usuario</label>
            <input type="text" />

            <label>Nombre completo</label>
            <input type="text" />

            <label>Correo electronico</label>
            <input type="text" />

            <label>Contraseña</label>
            <input type="text" />

            <button>Registrar</button>
        </form>
    </DefaultLayout>
    </>
}

export default Register