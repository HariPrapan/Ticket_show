from flask import Flask , render_template , request ,url_for ,session ,redirect

from models import *
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
app=Flask(__name__)

app.secret_key = 'agsuwhdwhjnkm'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myproject.db"

db.init_app(app)

app.app_context().push()

@app.route("/")
def first():
    return render_template("first.html")

@app.route("/home")
def home():
    if 'username' in session:
        sho = Show.query.all()
        ven = Venue.query.all()
        tickets = Booking.query.filter_by(user_name=session["username"])
        return render_template('home.html',show=sho,venue=ven,tickets=tickets,user=session["username"])
    else:
        return redirect(url_for('user_login'))

@app.route("/create_show" ,methods=["GET","POST"])
def show():
    if request.method == "POST":
        try:
            show_name = request.form["show"]
            ratings = request.form.get("rating")
            tags = request.form.get("tags")
            price = request.form.get("price")
            shift = request.form.get("shift")
            image_url=request.form.get("image_url")
            venue_id = request.form.get("venue_id")
            s1 = Show(show_name=show_name, Rating=ratings, Price=price, Tags=tags, shift=shift ,image_url=image_url)
            v1 = Venue.query.get(venue_id)
            db.session.add(s1)
            s1.venue.append(v1)
            db.session.commit()
            msg = "Show has been added successfuly"
            sho = Show.query.all()
            ven = Venue.query.all()
            return render_template("admin_dashboard.html", Message=msg, show=sho, venue=ven)

        except:
            error="Oops ! It seems that entered venue details does not exist , Please check."
            return render_template("show.html",error=error)

    if session["username"] == "Hari Prapan":
        return render_template("show.html")
    else:
        return redirect(url_for('admin_login'))

@app.route("/create_venue",methods=["GET","POST"])
def venue():
    if request.method=="POST":
        venue_name=request.form.get("venue")
        location=request.form.get("loc")
        capacity=request.form.get("cap")

        v1=Venue(venue_name=venue_name,venue_loc=location,capacity=capacity)
        db.session.add(v1)
        db.session.commit()
        msg = "Venue has been added successfuly"
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html",Message=msg,show=sho,venue=ven)

    if session["username"] == "Hari Prapan":
        return render_template("venue.html")
    else:
        return redirect(url_for('admin_login'))

@app.route("/venue_details")
def venue_details():
    return render_template("venue_details.html")

@app.route("/user_register",methods=(["GET","POST"]))
def user_register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        user=request.form.get("user")
        password=request.form.get("pass")
        try:
            u1 = User(username=user, password=password)
            db.session.add(u1)
            db.session.commit()
            msg = "Account created , please login."
            return render_template("login.html", Message=msg)
        except:
            msg="User exist ! Try with other username"
            return render_template("register.html",msg=msg)


@app.route("/user_login",methods=(["GET","POST"]))
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Login successful
            session['logged_in'] = True
            session["username"]=username
            return redirect("/home")
        else:
            # Login failed
            error = 'Invalid username or password. Try again'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route("/admin/login",methods=(["GET","POST"]))
def admin_login():
    if request.method=="GET":
        return render_template("admin_login.html")
    if request.method=="POST":
        try :
            admin = request.form.get("admin_id")
            password = request.form.get("pass")

            user = Admin.query.filter_by(admin=admin, password=password).first()
            if user:
                # login successful
                session['logged_in'] = True
                session['username'] = admin
                return redirect(url_for('admin_dashboard'))
            else:
                # login failed
                error = 'Invalid admin id or password. Try again'
                return render_template('admin_login.html', error=error)

        except:
            error = 'No admin exist , contact administrator'
            return render_template("admin_login.html" ,error=error)


@app.route("/delete_show/<int:id>",methods=(["GET","POST"]))
def del_show(id):
    if session["username"] == "Hari Prapan":
        s1 = Show.query.filter_by(show_id=id).first()
        db.session.delete(s1)
        db.session.commit()
        show_id=s1.show_id
        b1=Booking.query.filter_by(show_id=show_id)
        for booking in b1:
            db.session.delete(booking)
            db.session.commit()
        r1=Rate.query.filter_by(show_id=show_id)
        for rating in r1:
            db.session.delete(rating)
            db.session.commit()
        msg = "Show along with its any booked tickets got deleted successfully."
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html", Message=msg, show=sho, venue=ven)
    else:
        return render_template("admin_login.html")

@app.route("/edit_show/<int:show_id>",methods=(["GET","POST"]))
def edit_show(show_id):
    if request.method=="POST":
        show=Show.query.filter_by(show_id=show_id).first()
        show.show_name=request.form["show_name"]
        show.Price=request.form["show_price"]
        show.image_url=request.form["image_url"]
        show.Tags=request.form["tags"]
        db.session.add(show)
        db.session.commit()
        msg = "Show Updated succesffull."
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html", Message=msg, show=sho, venue=ven)

    show=Show.query.filter_by(show_id=show_id)
    return render_template("edit_show.html",show=show,show_id=show_id)

@app.route("/edit_venue/<int:venue_id>",methods=(["GET","POST"]))
def edit_venue(venue_id):
    if request.method=="POST":
        venue=Venue.query.filter_by(venue_id=venue_id).first()
        venue.venue_name=request.form["venue_name"]
        venue.venue_loc=request.form["venue_loc"]
        venue.capacity=request.form["capacity"]
        db.session.add(venue)
        db.session.commit()
        msg = "Venue Updated succesffull."
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html", Message=msg, show=sho, venue=ven)

    venue=Venue.query.filter_by(venue_id=venue_id)
    return render_template("edit_venue.html",venue=venue,venue_id=venue_id)


@app.route("/delete_venue/<int:id>",methods=(["GET","POST"]))
def del_venue(id):
    if session["username"] == "Hari Prapan":
        v1 = Venue.query.filter_by(venue_id=id).first()
        show=v1.show
        for show in show:
            r1 = Rate.query.filter_by(show_id=show.show_id)
            for rating in r1:
                db.session.delete(rating)
                db.session.commit()
            db.session.delete(show)
            db.session.commit()
        db.session.delete(v1)
        db.session.commit()
        msg = "Venue (along with their alloted shows if any) got deleted successfully."
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html", Message=msg, show=sho, venue=ven)
    else:
        return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if session["username"]=="Hari Prapan":
        sho = Show.query.all()
        ven = Venue.query.all()
        return render_template("admin_dashboard.html",show=sho,venue=ven)
    else:
        return redirect(url_for('admin_login'))

@app.route("/book/<string:show_name>/<int:show_id>" ,methods=(["GET","POST"]))
def booking_form(show_name,show_id):
    if request.method=="POST":
        tickets = request.form.get("tickets")
        venue=request.form.get("venue")
        show = Show.query.get(show_id)
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # login successful
            session['logged_in'] = True
            session['username'] = username
            booking = Booking(user_name=username, show_id=show_id, tickets=tickets,venue=venue,show_name=show_name)
            ticket=Booking.query.filter_by(show_id=show_id)
            count=0
            for tict in ticket:
                s=tict.tickets
                count=count+s

            show=Show.query.filter_by(show_id=show_id).first()
            v=show.venue

            for venue in v:
                c=venue.capacity

            if count<c:
                db.session.add(booking)
                db.session.commit()
                sho = Show.query.all()
                ven = Venue.query.all()
                tickets = Booking.query.filter_by(user_name=username)
                msg = "Booking successfull, please see your tickets below."
                return render_template("home.html", venue=ven, show=sho, tickets=tickets, user=username, msg=msg)
            else :
                sho = Show.query.all()
                ven = Venue.query.all()
                tickets = Booking.query.filter_by(user_name=username)
                error="Ops ! it seems like all tickets for the selected movie has been booked. Try booking for some other movie"
                return render_template("home.html",venue=ven, show=sho, tickets=tickets, user=username,msg=error)

        else:
            msg="Booking attempted by unregisterd person , Login to continue."
            return render_template("login.html",Message=msg)
    if request.method=="GET":
        sho=Show.query.filter_by(show_name=show_name)
        v = []
        for show in sho:
            venue = show.venue
            v.append(venue)
        return render_template("booking.html", show=sho,venue=v,show_name=show_name,show_id=show_id)

@app.route('/logout')
def logout():
    session.clear()
    message="Logout successfull"
    return render_template("login.html",message=message)

@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return render_template("first.html")

@app.route("/refresh/admin_dashboard")
def refresh_adm_dashboard():
    if session["username"] == "Hari Prapan":
        sho=Show.query.all()
        ven=Venue.query.all()
        return render_template("admin_dashboard.html",show=sho,venue=ven)
    else:
        error="You should login first."
        return render_template("admin_login.html",error=error)

@app.route("/search_movie",methods=(["GET","POST"]))
def search_movie():
    if request.method=="GET":
        if "username" in session:
            return render_template("search_movie.html")
        else:
            return "Go and login first"
    if request.method=="POST":
        if "username" in session:
            movie=request.form.get("movie")
            tags=request.form.get("tags")
            Movies=Show.query.filter_by(show_name=movie)
            show2 = Show.query.filter_by(Tags=tags)

            return render_template("searched_movie.html",show=Movies,show2=show2)
        else:
            return "Unauthorised access , Go to main dashboard to login"

@app.route("/search_venue",methods=(["GET","POST"]))
def search_venue():
    if request.method=="GET":
        if "username" in session:
            return render_template("search_venue.html")
        else:
            return "Go and login first"
    if request.method=="POST":
        if "username" in session:
            venue=request.form.get("venue")
            venue=Venue.query.filter_by(venue_name=venue)
            loc=request.form.get("loc")
            venue2=Venue.query.filter_by(venue_loc=loc)
            return render_template("searched_venue.html", venue=venue, venue2=venue2)

        else:
            return "Unauthorised access , Go to main dashboard to login"

@app.route("/performance/forecast/bookings")
def performance():

    show_ids=[]
    for booking in Booking.query.distinct(Booking.show_id).all():
        show_ids.append(booking.show_id)

    ticket_counts = []
    for show_id in show_ids:
        ticket_count = db.session.query(db.func.sum(Booking.tickets)).filter_by(show_id=show_id).scalar()
        ticket_counts.append(ticket_count or 0)

    plt.bar(show_ids, ticket_counts ,width=0.3)
    plt.title('Ticket Sales by Show')
    plt.xlabel('Show ID')
    plt.ylabel('Number of Tickets Sold')
    plt.xticks(show_ids, show_ids)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template('graph.html', graph_url=graph_url)

@app.route("/rating/<int:show_id>",methods=(["GET","POST"]))
def ratings_show(show_id):
    if request.method == "POST":
        if 'username' in session:
            a=Rate.query.filter_by(show_id=show_id,user_name=session["username"]).count()
            if a==0:
                ratings = request.form.get("rating")
                r1 = Rate(show_id=show_id, Rating=ratings, user_name=session["username"])
                db.session.add(r1)
                db.session.commit()
            else:
                r1 = Rate.query.filter_by(show_id=show_id,user_name=session["username"]).first()
                r1.Rating = request.form.get("rating")
                db.session.add(r1)
                db.session.commit()
            rat = Rate.query.filter_by(show_id=show_id)
            Rating_sum = 0
            for rating in Rate.query.distinct(Rate.show_id).all():
                Rating_sum = Rating_sum + rating.Rating
            count = Rate.query.distinct(Rate.show_id).count()

            rating = Rating_sum / count
            rating = round(rating, 2)
            show = Show.query.filter_by(show_id=show_id).first()
            show.Rating = rating
            db.session.add(show)
            db.session.commit()

            sho = Show.query.all()
            ven = Venue.query.all()
            tickets = Booking.query.filter_by(user_name=session["username"])
            msg = "Thanks for rating the show."
            return render_template('home.html', show=sho, venue=ven, tickets=tickets, user=session["username"],
                                   msg=msg)
        else:
            return redirect(url_for('user_login'))

    if request.method=="GET":
        if "username" in session:
            show = Show.query.filter_by(show_id=show_id)
            return render_template("Ratings.html", show_id=show_id, show=show)
        else:
            return redirect(url_for("user_login"))




