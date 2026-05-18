<script setup>
</script>

<template>

<footer class="cyber-footer">

    <div class="container">

        <div class="row justify-content-center">

            <!-- REDES -->
            <div class="col-12 text-center">

                <h6 class="footer-title">
                    Redes Sociales
                </h6>

                <div class="social-icons">

                    <a href="#">
                        <i class="fab fa-facebook-f"></i>
                    </a>

                    <a href="#">
                        <i class="fab fa-instagram"></i>
                    </a>

                    <a href="#">
                        <i class="fab fa-x-twitter"></i>
                    </a>

                    <a href="#">
                        <i class="fab fa-linkedin-in"></i>
                    </a>

                    <a href="#">
                        <i class="fab fa-github"></i>
                    </a>

                </div>

            </div>

        </div>

    </div>

</footer>

</template>

<style scoped>

/* =====================================================================================
   FOOTER
===================================================================================== */

.cyber-footer {
    background: #1f232a;

    border-top: 1px solid rgba(176, 38, 255, 0.15);
    border-radius: 2px;

    padding: 40px 0 20px;

    margin-top: 40px;

    position: sticky;
    bottom: 0;
    width: 100%;
}

/* =====================================================================================
   TITULO
===================================================================================== */
.footer-title {
    color: white;

    font-size: 1rem;
    font-weight: 600;

    margin-bottom: 18px;
}

/* =====================================================================================
   REDES SOCIALES
===================================================================================== */
.social-icons {
    display: flex;

    justify-content: center;
    align-items: center;

    gap: 14px;
}

.social-icons a {
    width: 45px;
    height: 45px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 12px;

    text-decoration: none;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    color: rgba(255,255,255,0.85);

    transition: all 0.3s ease;
}

.social-icons a:hover {
    transform: translateY(-4px);

    background: rgba(176, 38, 255, 0.15);

    border-color: rgba(176, 38, 255, 0.45);

    color: #b026ff;
}

.social-icons i {
    font-size: 1rem;
}

/* =====================================================================================
   COPYRIGHT
===================================================================================== */
.footer-bottom {
    border-top: 1px solid rgba(255,255,255,0.06);

    margin-top: 30px;
    padding-top: 20px;

    color: rgba(255,255,255,0.5);

    font-size: 0.9rem;
}

</style>