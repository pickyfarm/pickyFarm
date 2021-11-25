module.exports = {
    purge: {
        enabled: true,
        content: ['./templates/**/*.html'],
    },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            width: {
                header: '1280px',
                content: '990px',
            },

            height: {
                main: '750px',
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [],
};
