import pytest
import pygame
from main import Player, Ghost, Object, TILEWIDTH, TILEHEIGHT, increase_speed, reset_level
from board import boards as original_boards

# A simplified mock board for controlled testing
mock_level = [
    [4, 4, 4, 4, 4],
    [3, 1, 0, 2, 3],
    [3, 0, 4, 0, 3],
    [3, 1, 0, 1, 3],
    [4, 4, 4, 4, 4],
]


@pytest.fixture
def game_objects():
    """A pytest fixture to provide clean Player and Ghost objects for each unit test."""
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    player_images = [pygame.Surface((1, 1))]
    ghost_sprites = [pygame.Surface((1, 1))] * 6

    player = Player(screen, 1, 1, 1 * TILEWIDTH, 1 * TILEHEIGHT, 0, 0, player_images, 0, False, 0, 7)
    ghost = Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, 8)

    yield player, ghost
    pygame.quit()


def test_object_checkTurns(monkeypatch):
    """Unit test for the Object.checkTurns method."""
    # Arrange
    monkeypatch.setattr('game.level', mock_level)
    obj = Object(None, 1, 2)  # Positioned in an open space in mock_level

    # Act
    turns = obj.checkTurns()

    # Assert: Should be able to move in all directions
    assert turns == [True, True, True, True]

    # Arrange 2: Place object in a corner
    obj_corner = Object(None, 1, 1)

    # Act 2
    turns_corner = obj_corner.checkTurns()

    # Assert 2: Can only move right and down
    assert turns_corner == [True, False, False, True]


def test_player_checkCollisions_pellet(game_objects, monkeypatch):
    """Unit test for Player collision with a regular pellet."""
    # Arrange
    player, _ = game_objects
    # Create a mutable copy of the board for the test
    test_level = [row[:] for row in mock_level]
    monkeypatch.setattr('game.level', test_level)

    player._Object__row = 1
    player._Object__col = 1
    initial_points = player.points

    # Act
    player.checkCollisions()

    # Assert
    assert player.points == initial_points + 1
    assert test_level[1][1] == 0  # Pellet should be removed


def test_player_checkCollisions_power_pellet(game_objects, monkeypatch):
    """Unit test for Player collision with a power pellet."""
    # Arrange
    player, _ = game_objects
    test_level = [row[:] for row in mock_level]
    monkeypatch.setattr('game.level', test_level)

    player._Object__row = 1
    player._Object__col = 3
    initial_points = player.points

    # Act
    player.checkCollisions()

    # Assert
    assert player.points == initial_points + 10
    assert player.power is True
    assert player.power_counter == 0
    assert test_level[1][3] == 0  # Power pellet should be removed


def test_player_powerUp_lifecycle(game_objects):
    """Unit test for the power-up timer and state change."""
    # Arrange
    player, _ = game_objects
    player.power = True
    player.power_counter = 599  # Set counter just before expiry

    # Act 1: Increment counter one step
    player.powerUp()

    # Assert 1: Power should still be active
    assert player.power is True
    assert player.power_counter == 600

    # Act 2: Increment again to trigger expiry
    player.powerUp()

    # Assert 2: Power should be disabled and counter reset
    assert player.power is False
    assert player.power_counter == 0


def test_ghost_findPath_chase_logic(game_objects, monkeypatch):
    """Unit test for Ghost's chase pathfinding logic."""
    # Arrange
    player, ghost = game_objects
    monkeypatch.setattr('game.level', mock_level)
    monkeypatch.setattr('random.random', lambda: 1.0)  # Disable randomness

    player._Object__row, player._Object__col = 3, 2  # Player is below ghost
    ghost._Object__row, ghost._Object__col = 1, 2  # Ghost is at (1, 2)

    # Act
    direction = ghost.findPath(player.readRow(), player.readCol())

    # Assert: Ghost should move down (3) towards the player
    assert direction == 3


def test_ghost_findPath_flee_logic(game_objects, monkeypatch):
    """Unit test for Ghost's flee pathfinding logic."""
    # Arrange
    player, ghost = game_objects
    monkeypatch.setattr('game.level', mock_level)
    monkeypatch.setattr('random.random', lambda: 1.0)  # Disable randomness

    player.power = True
    player._Object__row, player._Object__col = 1, 2  # Player is at (1, 2)
    ghost._Object__row, ghost._Object__col = 3, 2  # Ghost is at (3, 2)
    # Flee target for ghost 0 is (2, 2) in the main game, but we test general flee logic
    # The ghost should move away from the player. Its corner is top-left (2,2 in original board)
    # From (3,2) it should move up to get away from player and towards its corner.

    # Act
    direction = ghost.findPath(player.readRow(), player.readCol())

    # Assert: Ghost should move up (2) away from the player
    assert direction == 2


def test_increase_speed_logic(monkeypatch):
    """Unit test for the global increase_speed function."""
    # Arrange
    # Mock the global speed variables and a dummy player/ghosts list
    monkeypatch.setattr('game.player_speed', 7)
    monkeypatch.setattr('game.ghost_speed', 8)

    mock_player = Player(None, 0, 0, 0, 0, 0, 0, [], 0, False, 0, 7)
    mock_ghost = Ghost(None, 0, 0, 0, 0, 0, None, False, False, [], 0, 8)
    monkeypatch.setattr('game.player', mock_player)
    monkeypatch.setattr('game.ghosts', [mock_ghost])

    # Act
    increase_speed()

    # Assert
    assert mock_player.player_speed == 6
    assert mock_ghost.speed == 7


def test_increase_speed_stops_at_minimum(monkeypatch):
    """Unit test to ensure speed does not decrease below the minimum."""
    # Arrange
    monkeypatch.setattr('game.player_speed', 3)
    monkeypatch.setattr('game.ghost_speed', 3)

    mock_player = Player(None, 0, 0, 0, 0, 0, 0, [], 0, False, 0, 3)
    mock_ghost = Ghost(None, 0, 0, 0, 0, 0, None, False, False, [], 0, 3)
    monkeypatch.setattr('game.player', mock_player)
    monkeypatch.setattr('game.ghosts', [mock_ghost])

    # Act
    increase_speed()

    # Assert
    assert mock_player.player_speed == 3
    assert mock_ghost.speed == 3