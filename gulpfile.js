// Konrad Maciejczyk, 2021-2022
var gulp = require('gulp');
var sass = require('gulp-sass')(require('sass'));
var browserSync = require('browser-sync').create();

const app_name= "worker_side";

function style(){
    //1. Where SCSS files are
    return gulp.src('./scss/' + app_name + '/*.scss')
    //2. Passing that file through sass compiler
    .pipe(sass())
    //3. Where should compiled files be saved
    .pipe(gulp.dest('./' + app_name + '/static/' + app_name + '/css/'))
}

function watch(){
    browserSync.init({
        port: 8000,
        proxy: 'localhost:8000',
        browser: "firefox"
    });
    gulp.watch('./scss/' + app_name + '/*.scss', style);
    gulp.watch('./'+ app_name +'/templates/'+ app_name +'/*.html').on('change', browserSync.reload);
    gulp.watch('./'+ app_name +'/static/'+ app_name +'/*.js').on('change', browserSync.reload);
    gulp.watch('./'+ app_name +'/static/'+ app_name +'/css/*.css').on('change', browserSync.reload);
}

exports.style = style;
exports.watch = watch;