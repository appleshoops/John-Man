import pytest
import pygame
import random
from game import Player, Ghost, TILEWIDTH, TILEHEIGHT
from board import boards as original_boards


def set_pos(obj, row, col):
    """Helper function to set an object's grid and pixel positions."""
    obj._Object__row = row
    obj._Object__col = col
    obj._Object__xPos = col * TILEWIDTH
    obj._Object__yPos = row * TILEHEIGHT


@pytest.fixture
def game_setup(monkeypatch):
    """A pytest fixture to set up a clean game state for each grey-box test."""
    # Disable randomness in ghost AI for deterministic tests
    monkeypatch.setattr('random.random', lambda: 1.0)

    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    # Import the game module to access its global variables
    import game
    game.level = [row.copy() for row in original_boards]

    # Setup player with a dummy sprite to prevent errors
    player_images = [pygame.Surface((1, 1))]
    player = Player(screen, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, 0, player_images, 0, False, 0, 7)
    game.player = player

    # Setup ghosts
    ghost_sprites = [pygame.Surface((1, 1))] * 6  # Dummy sprites
    ghosts = [
        Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 2, 27, 27 * TILEWIDTH, 2 * TILEHEIGHT, 1, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 30, 2, 2 * TILEWIDTH, 30 * TILEHEIGHT, 2, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 30, 27, 27 * TILEWIDTH, 30 * TILEHEIGHT, 3, player, False, False, ghost_sprites, 0, 8)
    ]
    game.ghosts = ghosts

    yield player, ghosts, game.level

    pygame.quit()


def test_ghost_ai_state_transition(game_setup):
    """Verify a ghost transitions from chase -> flee -> chase mode."""
    player, ghosts, _ = game_setup
    blinky = ghosts[0]

    # Arrange: Place player and ghost near each other
    set_pos(player, 20, 15)
    set_pos(blinky, 20, 18)

    # Act 1: Check initial chase behavior. Ghost should move towards player (left).
    direction_chase = blinky.findPath(player.readRow(), player.readCol())
    assert direction_chase == 1  # 1 is Left

    # Act 2: Player eats a power pellet.
    player.power = True

    # Assert 1: Ghost should now flee towards its corner (2,2), so it should move up or left.
    direction_flee = blinky.findPath(player.readRow(), player.readCol())
    assert direction_flee in [1, 2]  # 1 is Left, 2 is Up

    # Act 3: Expire the power-up.
    player.power_counter = 600
    player.powerUp()
    assert player.power is False

    # Assert 2: Ghost should return to chase mode.
    direction_chase_again = blinky.findPath(player.readRow(), player.readCol())
    assert direction_chase_again == 1  # 1 is Left


def test_ghost_eaten_and_respawn(game_setup):
    """Verify the full sequence of a ghost being eaten and resetting."""
    player, ghosts, _ = game_setup
    blinky = ghosts[0]
    initial_points = player.points

    # Arrange: Give player power-up and place ghost at the same location
    player.power = True
    set_pos(player, 5, 5)
    set_pos(blinky, 5, 5)

    # Create rects for collision detection. This is needed because drawSprite() is not called.
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    blinky.rect = pygame.Rect(blinky.readCentreXPos() - 18, blinky.readCentreYPos() - 18, 36, 36)

    # Act 1: Player collides with ghost
    player.checkGhostCollisions()

    # Assert 1: Ghost is marked as eaten, player gains points, ghost is sent to its corner
    assert player.eaten_ghosts[0] is True
    assert player.points == initial_points + 100
    assert blinky.mortality is True
    assert (blinky.readRow(), blinky.readCol()) == (2, 2)  # Its respawn corner

    # Act 2: Expire the power-up
    player.power_counter = 600
    player.powerUp()

    # Assert 2: Ghost's mortality is reset
    assert blinky.mortality is False


def test_player_life_loss_and_reset(game_setup):
    """Verify player loses a life and resets position upon collision without power-up."""
    player, ghosts, _ = game_setup
    blinky = ghosts[0]
    initial_lives = player.lives

    # Arrange: Place player and ghost at the same spot, no power-up
    player.power = False
    set_pos(player, 5, 5)
    set_pos(blinky, 5, 5)

    # Create rects for collision
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    blinky.rect = pygame.Rect(blinky.readCentreXPos() - 18, blinky.readCentreYPos() - 18, 36, 36)

    # Act: Trigger collision
    player.checkGhostCollisions()

    # Assert: Player loses a life and position is reset
    assert player.lives == initial_lives - 1
    assert (player.readRow(), player.readCol()) == (18, 15)  # Default start position


def test_pinky_ambush_ai(game_setup):
    """Grey-box test for Ghost 1 (Pinky) AI.
    It should target 4 tiles ahead of the player."""
    player, ghosts, _ = game_setup
    pinky = ghosts[1]

    # Arrange: Place player and Pinky, set player direction to right
    set_pos(player, 22, 10)
    player.direction = 0  # Moving Right
    set_pos(pinky, 22, 18)

    # Act: Pathfind. Pinky should target (22, 14), which is 4 tiles ahead of player.
    # The shortest path to (22, 14) is to move left.
    direction = pinky.findPath(player.readRow(), player.readCol())

    # Assert: Pinky moves left to intercept.
    assert direction == 1  # 1 is Left


def test_inky_flanking_ai(game_setup):
    """Grey-box test for Ghost 2 (Inky) AI.
    It targets a point based on both player and Blinky's positions."""
    player, ghosts, _ = game_setup
    blinky = ghosts[0]
    inky = ghosts[2]

    # Arrange:
    set_pos(player, 22, 15)
    set_pos(blinky, 20, 15)
    set_pos(inky, 26, 17)

    # Act:
    # The vector from Blinky to Player is (2, 0).
    # Target is Player pos + vector = (22+2, 15+0) = (24, 15).
    # Inky is at (26, 17). To get to (24, 15), it must move left or up.
    # The algorithm prefers left (index 1) over up (index 2).
    direction = inky.findPath(player.readRow(), player.readCol())

    # Assert: Inky moves left towards the calculated target point.
    assert direction == 1  # 1 is Left