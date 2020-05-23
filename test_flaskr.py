import unittest
from unittest.mock import Mock
import json
import datetime

from flaskr.init import create_app
from models import set_up, db, Movie, Actor

# Initialise Authentication Token For Testing
t1 = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZHdmlrTTZaMGRWdUJwZUdMU3lWVSJ9"
t2 = "eyJpc3MiOiJodHRwczovL2NhcHN0b25lLXByb2plY3Qtc2F0YXMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzU4NzNjMjU0YmE3MGJmNDgzYjM5NiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkwMjM5Mzc1LCJleHAiOjE1OTAzMjU3NzUsImF6cCI6Inl0dFhFNVJMd3cwWlptVDFZcVRkcW1zMWI1Nk9RM3RqIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19"
t3 = "IGVQI7ps2n-tBNAHjih8cjZDznmrT5DwQ__wcIzQoWnfo_H48PgYU4Qp7oycifoUmZfXFdNtSBwKr0pERg1rG90Vxri_tXBM0HhnnvyGEJZ890LiNFYx8-kdHqeevgA-5tmDQ5hdZSjXO7_bQhtGHSSTgBQrFivufWPoeG3woSWkRUsXYtAgJob4QJVZwuEOnixLsvnFuBzq7poeuoqRrSXoOBZbrd_t8K0Wgf4CI5xoG0NimFjEbMATIcYqKMXnSKjVwmp8jKI32n9zbET-IBxAf0ToEEjMaEZAfkZv5TTDPN8DXKSYV16jK6c2oRSCTss9I7Eo-vmv36zdhr2iFA"
auth_token = "{}.{}.{}".format(t1, t2, t3)


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        set_up(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Get Actors
    def test_get_actors(self):
        # Testing a successful get request for actors
        res = self.client().get(
            'https://capstone-project-satas.herokuapp.com/actors',
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]["age"])
        self.assertTrue(data[0]["gender"])
        self.assertTrue(data[0]["name"])
        self.assertTrue(data[0]["id"])

    def test_503_actors(self):
        # Testing a failed get request for actors, database connectivity issues
        requests = Mock()
        requests.get.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            res = requests.get(
                'https://capstone-project-satas.herokuapp.com/actors',
                headers={'Authorization': 'Bearer ' + auth_token}
            )
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 503)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'issues communicating with the database')
            self.assertEqual(data['error'], 503)

    # Get Movies
    def test_get_movies(self):
        # Testing a successful get request for movies
        res = self.client().get(
            'https://capstone-project-satas.herokuapp.com/movies',
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data[0]["title"])
        self.assertTrue(data[0]["release_date"])
        self.assertTrue(data[0]["id"])

    def test_503_movies(self):
        # Testing a failed get request for movies, database connectivity issues
        requests = Mock()
        requests.get.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            res = requests.get(
                'https://capstone-project-satas.herokuapp.com/movies',
                headers={'Authorization': 'Bearer ' + auth_token}
                )
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 503)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'issues communicating with the database')
            self.assertEqual(data['error'], 503)

    # Delete a Movie
    def test_delete_movie(self):
        # Testing a movie deletion
        latest_movie = Movie.query.order_by(db.desc(Movie.id)).first()

        res = self.client().delete(
            'https://capstone-project-satas.herokuapp.com/movies/'+str(latest_movie.id),
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], latest_movie.id)

    def test_404_delete_movie(self):
        # Testing a fail in deleting a movie, due to it not existing
        res = self.client().delete(
            'https://capstone-project-satas.herokuapp.com/movies/10000',
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    # Delete an Actor
    def test_delete_actor(self):
        # Testing an actor deletion
        latest_actor = Actor.query.order_by(db.desc(Actor.id)).first()
        res = self.client().delete(
            'https://capstone-project-satas.herokuapp.com/actors/'+str(latest_actor.id),
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], latest_actor.id)

    def test_404_delete_actor(self):
        # Testing a fail in deleting an actor
        res = self.client().delete(
            'https://capstone-project-satas.herokuapp.com/actors/10000',
            headers={'Authorization': 'Bearer ' + auth_token}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    # Post a Movie
    def test_post_503_movies(self):
        # Testing a failed post request for movies, database connectivity issues
        requests = Mock()
        requests.post.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            res = requests.post(
                'https://capstone-project-satas.herokuapp.com/movies',
                headers={'Authorization': 'Bearer ' + auth_token},
                json={
                    "title": "Testing a post of a movie",
                    "release_date": "21 May, 2020"
                }
            )

            data = json.loads(res.data)
            self.assertEqual(res.status_code, 503)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'issues communicating with the database')
            self.assertEqual(data['error'], 503)

    def test_post_movie(self):
        # Testing a movie post
        res = self.client().post(
            'https://capstone-project-satas.herokuapp.com/movies',
            headers={'Authorization': 'Bearer ' + auth_token},
            json={
                "title": "Unit Testing a post of a movie",
                "release_date": "11 JANUARY, 2011"
            }
        )

        added_movie = Movie.query.filter_by(title='Unit Testing a post of a movie').first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(added_movie.title, 'Unit Testing a post of a movie')
        self.assertEqual(added_movie.release_date, datetime.date(2011, 1, 11))

    # Post an Actor
    def test_post_503_actor(self):
        # Testing a failed post request for actors, database connectivity issues
        requests = Mock()
        requests.post.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            res = requests.post(
                'https://capstone-project-satas.herokuapp.com/actors',
                headers={'Authorization': 'Bearer ' + auth_token},
                json={
                    "name": "Unit testing an actor post",
                    "age": 67,
                    "gender": "M"
                }
            )

            data = json.loads(res.data)
            self.assertEqual(res.status_code, 503)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'issues communicating with the database')
            self.assertEqual(data['error'], 503)

    def test_post_actor(self):
        # Testing an actor post
        res = self.client().post(
           'https://capstone-project-satas.herokuapp.com/actors',
           headers={'Authorization': 'Bearer ' + auth_token},
           json={
                "name": "Unit testing an actor post",
                "age": 67,
                "gender": "M"
            }
        )

        added_actor = Actor.query.filter_by(name='Unit testing an actor post').first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(added_actor.name, 'Unit testing an actor post')
        self.assertEqual(added_actor.age, 67)
        self.assertEqual(added_actor.gender, "M")

    # Patch a Movie
    def test_patch_movie(self):
        # Testing a movie patch
        res = self.client().patch(
            'https://capstone-project-satas.herokuapp.com/movies/36',
            headers={'Authorization': 'Bearer ' + auth_token},
            json={
                "title": "Unit testing a patch of a movie",
                "release_date": "22 May, 2020"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], "Unit testing a patch of a movie")

    def test_404_patch_movie(self):
        # Testing a fail in patching a movie, due to it not existing
        res = self.client().patch(
            'https://capstone-project-satas.herokuapp.com/movies/1000',
            headers={'Authorization': 'Bearer ' + auth_token},
            json={
                "title": "Unit testing a patch of a movie",
                "release_date": "22 May, 2020"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)

    # Patch an Actor
    def test_patch_actor(self):
        # Testing an actor patch
        res = self.client().patch(
            'https://capstone-project-satas.herokuapp.com/actors/16',
            headers={'Authorization': 'Bearer ' + auth_token},
            json={
                "name": "Unit testing an actor post",
                "age": 67,
                "gender": "M"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], "Unit testing an actor post")

    def test_404_patch_actor(self):
        # Testing a fail in patching an actor, due to it not existing
        res = self.client().patch(
            'https://capstone-project-satas.herokuapp.com/actors/1000',
            headers={'Authorization': 'Bearer ' + auth_token},
            json={
                "name": "Unit testing an actor post",
                "age": 67,
                "gender": "M"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
