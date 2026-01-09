const indexRoutes = require('./index');
const authRoutes = require('./auth');

module.exports = (app) => {
    app.use('/', indexRoutes);
    app.use('/', authRoutes);
};
