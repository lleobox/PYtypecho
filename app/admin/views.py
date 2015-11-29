# coding: utf-8
from flask import render_template, redirect, flash, request, url_for, session
from flask.ext.login import login_required
from . import admin
from .forms import postForm, pageForm, categoryForm, userForm
from ..modules import Post, Page, Category, User
from datetime import datetime


@admin.route("/main")
@login_required
def main():
    return render_template("admin/main.html")


# 文章相关内容
@admin.route("/write-post", methods=["GET", "POST"])
@login_required
def write_post():
    form = postForm()
    categories = Category.objects()
    if form.validate_on_submit():
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]
        tags = form.tags.data.split(",")
        author = session["username"]
        category = request.form['category']
        post = Post(title=title, slug=slug, text=text, tags=tags, author=author, category=category)
        if request.form["submit"] == "save":
            post.status = False
            post.save()
            if slug == "":
                post.slug = str(post.id)
                post.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_post"))
        else:
            post.status = True
            post.save()
            if slug == "":
                post.slug = str(post.id)
                post.save()
            flash(u"发布文章成功", "success")
            return redirect(url_for("admin.manage_posts"))
    return render_template("admin/write-post.html", form=form, categories=categories)


@admin.route("/manage-posts")
@login_required
def manage_posts():
    posts = Post.objects()
    categories = Category.objects(parent="")
    createds = []
    delays = []
    for post in posts:
        createds.append(post.created.strftime("%Y-%m-%d"))
        delay = (datetime.now() - post.created).seconds/60
        delays.append(delay)
    return render_template("admin/manage-posts.html", posts=posts,
                           delays=delays, createds=createds,
                           categories=categories)


@admin.route("/delete-posts", methods=["GET", "POST"])
@login_required
def delete_posts():
    slugs = request.form.getlist('slug')
    for slug in slugs:
        post = Post.objects(slug=slug)
        post.delete()
    flash(u"文章删除成功", "success")
    return redirect(url_for('admin.manage_posts'))


# 页面相关内容
@admin.route("/write-page", methods=["GET", "POST"])
@login_required
def write_page():
    form = pageForm()
    if form.validate_on_submit():
        title = form.title.data
        slug = form.slug.data
        text = request.form["edit-area-markdown-doc"]
        author = session["username"]
        page = Page(title=title, slug=slug, text=text, author=author)
        if request.form["submit"] == "save":
            page.status = False
            page.save()
            if slug == "":
                page.slug = str(post.id)
                page.save()
            flash(u"保存草稿成功", "success")
            return redirect(url_for("admin.write_page"))
        else:
            page.status = True
            page.save()
            if slug == "":
                page.slug = str(post.id)
                page.save()
            flash(u"发布页面成功", "success")
            return redirect(url_for("admin.manage_pages"))
    return render_template("admin/write-page.html", form=form)


@admin.route('/manage-pages')
@login_required
def manage_pages():
    pages = Page.objects()
    createds = []
    for page in pages:
        createds.append(page.created.strftime("%Y-%m-%d"))
    return render_template("admin/manage-pages.html", pages=pages, createds=createds)


@admin.route('/delete-pages', methods=["GET", "POST"])
@login_required
def delete_pages():
    slugs = request.form.getlist('slug')
    for slug in slugs:
        page = Page.objects(slug=slug)
        page.delete()
    flash(u"页面删除成功", "success")
    return redirect(url_for('admin.manage_pages'))


# 分类相关
@admin.route("/manage-categories")
@login_required
def manage_categories():
    categories = Category.objects()
    return render_template("admin/manage-categories.html", categories=categories)


@admin.route("/category", methods=["GET", "POST"])
@login_required
def category():
    cid = request.args.get("cid")

    if cid is not None:
        categories = Category.objects(id=cid)
        oldCategory = categories[0]
        form = categoryForm(name=oldCategory.name, slug=oldCategory.slug, description=oldCategory.description)
        return render_template("admin/categories.html", form=form)

    categories = Category.objects()
    choices = []
    for category in categories():
        choices.append((category.id, category.name))
    form = categoryForm()
    form.setChoices(choices)
    if form.validate_on_submit():
        slug = form.slug.data or form.name.data
        categories = Category(name=form.name.data, slug=slug, parent=request.form.get("parent" or ""))
        categories.save()
        flash(u"分类保存成功", "success")
        return redirect(url_for("admin.manage_categories"))
    return render_template("admin/categories.html", form=form)


@admin.route("/delete-categories", methods=["POST"])
@login_required
def delete_categories():
    cids = request.form.getlist('cid')
    for cid in cids:
        category = Category.objects(id=cid)
        category.delete()
    flash(u"分类删除成功", "success")
    return redirect(url_for('admin.manage_categories'))


# 用户相关
@admin.route("/users", methods=["GET", "POST"])
@login_required
def users():
    form = userForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data, url=form.url.data,
                    screenName=form.screenName.data, group=form.group.data)
        user.password = form.password.data
        user.save()
        flash(u"用户添加成功", "success")
        return redirect(url_for("admin.manage_users"))
    return render_template("admin/users.html", form=form)


@admin.route("/manage-users", methods=["GET", "POST"])
@login_required
def manage_users():
    users = User.objects()
    return render_template("admin/manage-users.html", users=users)


@admin.route("/delete-users", methods=["GET", "POST"])
@login_required
def delete_users():
    uids = request.form.getlist('uid')
    for uid in uids:
        user = User(id=uid)
        user.delete()
    flash(u"用户删除成功", "success")
    return redirect(url_for('admin.manage_users'))



@admin.route("/manage-comments")
@login_required
def manage_comments():
    return "pass"