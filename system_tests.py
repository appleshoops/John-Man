import pytest
import pygame
import game
from game import Player, Ghost, TILEWIDTH, TILEHEIGHT, check_level_complete
from board import boards as original_boards

def set_pos(obj, row, col):
    """Helper function to set both grid and pixel positions for a game object."""
    obj._Object__row = row
    obj._Object__col = col
    obj._Object__xPos = col * TILEWIDTH
    obj._Object__yPos = row * TILEHEIGHT

@pytest.fixture
def game_system_setup(monkeypatch):
    """A pytest fixture to set up a full game environment for system-level testing."""
    pygame.init()
    # Mock the screen to avoid creating a window during tests
    screen = pygame.display.set_mode((1, 1))

    # Create a mutable copy of the board for tests to modify
    test_level = [row[:] for row in original_boards]
    monkeypatch.setattr(game, 'level', test_level)

    # Setup Player and mock it into the game module
    player_images = [pygame.Surface((1, 1))]
    player = Player(screen, 18, 15, 15 * TILEWIDTH, 18 * TILEHEIGHT, 0, 0, player_images, 0, False, 0, 7)
    monkeypatch.setattr(game, 'player', player)

    # Setup Ghosts and mock them into the game module
    ghost_sprites = [pygame.Surface((1, 1))] * 6
    ghosts = [
        Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, 8),
        Ghost(screen, 2, 27, 27 * TILEWIDTH, 2 * TILEHEIGHT, 1, player, False, False, ghost_sprites, 0, 8)
    ]
    monkeypatch.setattr(game, 'ghosts', ghosts)

    # Mock global game state variables
    monkeypatch.setattr(game, 'player_speed', 7)
    monkeypatch.setattr(game, 'ghost_speed', 8)
    monkeypatch.setattr(game, 'running', True)

    yield player, ghosts, test_level

    pygame.quit()

def test_player_loses_life_system(game_system_setup):
    """
    System Test: Verify that the player loses a life and resets position
    when colliding with a ghost while not powered up.
    """
    player, ghosts, _ = game_system_setup
    blinky = ghosts[0]
    initial_lives = player.lives

    # Arrange: Place player and ghost on the same tile to force a collision.
    # Ensure player is not powered up and ghost is not mortal.
    player.power = False
    blinky.mortality = False
    set_pos(player, 5, 5)
    set_pos(blinky, 5, 5)
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    blinky.rect = pygame.Rect(blinky.readCentreXPos() - 18, blinky.readCentreYPos() - 18, 36, 36)

    # Act: Simulate the part of the game loop that checks for ghost collisions.
    player.checkGhostCollisions()

    # Assert: Verify life is lost and player is reset to start.
    assert player.lives == initial_lives - 1
    assert (player.readRow(), player.readCol()) == (18, 15)

def test_full_level_clear_and_reset_system(game_system_setup):
    """
    System Test: Verify that clearing all pellets triggers a level reset,
    resets entity positions, and increases game speed.
    """
    player, ghosts, level = game_system_setup
    initial_player_speed = game.player_speed
    initial_ghost_speed = game.ghost_speed

    # Arrange: Clear the board of all pellets except one.
    for r in range(len(level)):
        for c in range(len(level[r])):
            if level[r][c] in [1, 2]:
                level[r][c] = 0
    level[2][2] = 1  # Place one last pellet.
    set_pos(player, 2, 2)

    # Act: Simulate the game loop sequence for eating the last pellet and checking level completion.
    player.checkCollisions()
    check_level_complete()

    # Assert: Verify that the game state has been reset and updated correctly.
    # 1. Speeds are increased (values are decreased).
    assert game.player_speed == initial_player_speed - 1
    assert game.ghost_speed == initial_ghost_speed - 1

    # 2. Player and ghosts are reset to their starting positions.
    assert (player.readRow(), player.readCol()) == (18, 15)
    assert (ghosts[0].readRow(), ghosts[0].readCol()) == (2, 2)

    # 3. The level board is reloaded from the original template.
    assert game.level[2][3] == 1  # Check a known pellet location is restored.

def test_game_over_system(game_system_setup):
    """
    System Test: Verify that the game ends when the player loses their last life.
    """
    player, ghosts, _ = game_system_setup
    blinky = ghosts[0]

    # Arrange: Set player lives to 1 and force a collision.
    player.lives = 1
    player.power = False
    blinky.mortality = False
    set_pos(player, 5, 5)
    set_pos(blinky, 5, 5)
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    blinky.rect = pygame.Rect(blinky.readCentreXPos() - 18, blinky.readCentreYPos() - 18, 36, 36)

    # Act: Simulate the collision check that should trigger the game over.
    player.checkGhostCollisions()

    # Assert: The global 'running' flag in the game module should be set to False.
    assert game.running is False