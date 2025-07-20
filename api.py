from flask import jsonify ,request ,abort
from main import app
from models import *


@app.route('/api/all_venues', methods=['GET'])
def api_all_venues():
    venues = Venue.query.all()
    return jsonify([{ "venue_id":v.venue_id , 'venue_name': v.venue_name , 'venue_loc': v.venue_loc ,"capacity":v.capacity} for v in venues])

@app.route("/api/edit_venue/<int:venue_id>",methods=(["PUT"]))
def api_edit_venue(venue_id):
    venue = Venue.query.filter_by(venue_id=venue_id).first()
    if not venue:
        abort(404)
    venue.venue_name = request.json["venue_name"]
    venue.venue_loc = request.json["venue_loc"]
    venue.capacity = request.json["capacity"]
    db.session.add(venue)
    db.session.commit()
    ven = Venue.query.filter_by(venue_id=venue_id).first()
    return jsonify({"id":ven.venue_id,"venue_name":ven.venue_name,"capacity":ven.capacity,"Location":ven.venue_loc})

@app.route("/api/edit_show/<int:show_id>",methods=(["PUT"]))
def api_edit_show(show_id):
    show=Show.query.filter_by(show_id=show_id).first()
    if not show:
        abort(400)
    show.show_name=request.json["show_name"]
    show.Price=request.json["show_price"]
    show.Tags=request.json["show_tag"]
    db.session.add(show)
    db.session.commit()
    show = Show.query.filter_by(show_id=show_id).first()
    return jsonify({"id":show.show_id,"Name":show.show_name,"Price":show.Price,"Tags":show.Tags})


@app.route("/api/all_shows",methods=["GET"])
def api_all_shows():
    shows=Show.query.all()
    return jsonify([{"id":show.show_id,"show":show.show_name,"Rating":show.Rating,"Tags":show.Tags} for show in shows])


@app.route('/api/delete_venue/<int:id>', methods=['DELETE'])
def api_delete_venue(id):
    v1 = Venue.query.filter_by(venue_id=id).first()
    if not v1:
        abort(404)
    show = v1.show
    for show in show:
        db.session.delete(show)
        db.session.commit()
    db.session.delete(v1)
    db.session.commit()
    return jsonify({"message":'Venue (along with their alloted shows if any) got deleted successfully.'})

@app.route("/api/delete_show/<int:id>",methods=["DELETE"])
def api_delete_show(id):
    s1=Show.query.filter_by(show_id=id).first()
    if not s1:
        abort(400)
    db.session.delete(s1)
    db.session.commit()
    return jsonify({"Message":"Show got deleted successfully"})

@app.route('/api/create_show', methods=['POST'])
def api_create_show():
    show_name = request.json.get('show')
    ratings = request.json.get("rating")
    tags = request.json.get("tags")
    price = request.json.get("price")
    shift = request.json.get("shift")
    image_url = request.json.get("image_url")
    venue_id = request.json.get('venue_id')
    if not show_name or not venue_id:
        abort(400)
    show = Show(show_name=show_name, Rating=ratings, Price=price, Tags=tags, shift=shift ,image_url=image_url)
    v1 = Venue.query.get(venue_id)
    show.venue.append(v1)
    db.session.add(show)
    db.session.commit()
    return jsonify({'id': show.show_id, 'name': show.show_name, "Price":show.Price , "Rating":show.Rating ,"Tags":show.Tags})

@app.route("/api/create_venue",methods=["POST"])
def api_create_venue():
    venue_name = request.json.get("venue")
    location = request.json.get("loc")
    capacity = request.json.get("cap")
    v1 = Venue(venue_name=venue_name, venue_loc=location, capacity=capacity)
    db.session.add(v1)
    db.session.commit()
    return jsonify({"id":v1.venue_id,"Venue_name":v1.venue_name,"Location":v1.venue_loc,"capacity":v1.capacity})

if __name__=="__main__":
    app.run(debug=True)


